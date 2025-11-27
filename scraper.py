import asyncio
import aiohttp
import csv
import logging
import signal
import sys
from datetime import datetime
from typing import List, Dict, Optional, Set
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class UmicoScraper:
    """Crash-proof async scraper for Umico discount products with checkpoint/resume support"""

    def __init__(self, max_concurrent_requests: int = 10):
        self.base_url = "https://mp-catalog.umico.az/api/v1/products"
        self.params = {
            "per_page": 24,
            "with_discount": "true",
            "sort": "discount_score_desc"
        }
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "az",
            "content-language": "az",
            "origin": "https://birmarket.az",
            "referer": "https://birmarket.az/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        }
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.session: Optional[aiohttp.ClientSession] = None
        self.total_products = 0
        self.scraped_count = 0
        self.failed_pages: List[int] = []
        self.completed_pages: Set[int] = set()
        self.checkpoint_file = 'scraper_checkpoint.json'
        self.should_stop = False

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.warning(f"Received signal {signum}. Initiating graceful shutdown...")
        self.should_stop = True

    async def __aenter__(self):
        """Async context manager entry"""
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=10)
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            timeout=timeout,
            connector=connector
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

        # Save checkpoint on exit
        if exc_type is not None:
            logger.error(f"Exiting due to exception: {exc_type.__name__}: {exc_val}")
            self.save_checkpoint()

    def save_checkpoint(self):
        """Save current progress to checkpoint file"""
        checkpoint = {
            'completed_pages': list(self.completed_pages),
            'failed_pages': self.failed_pages,
            'scraped_count': self.scraped_count,
            'total_products': self.total_products,
            'timestamp': datetime.now().isoformat()
        }

        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)
            logger.info(f"Checkpoint saved: {len(self.completed_pages)} pages completed")
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")

    def load_checkpoint(self) -> bool:
        """Load progress from checkpoint file"""
        checkpoint_path = Path(self.checkpoint_file)

        if not checkpoint_path.exists():
            logger.info("No checkpoint found. Starting fresh.")
            return False

        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoint = json.load(f)

            self.completed_pages = set(checkpoint.get('completed_pages', []))
            self.failed_pages = checkpoint.get('failed_pages', [])
            self.scraped_count = checkpoint.get('scraped_count', 0)
            self.total_products = checkpoint.get('total_products', 0)

            logger.info(f"Checkpoint loaded: {len(self.completed_pages)} pages already completed")
            logger.info(f"Resuming from where we left off at {checkpoint.get('timestamp')}")
            return True
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return False

    def clear_checkpoint(self):
        """Remove checkpoint file after successful completion"""
        try:
            Path(self.checkpoint_file).unlink(missing_ok=True)
            logger.info("Checkpoint file cleared")
        except Exception as e:
            logger.error(f"Failed to clear checkpoint: {e}")

    async def fetch_page(self, page: int, retry_count: int = 5) -> Optional[Dict]:
        """Fetch a single page with retry logic and exponential backoff"""
        async with self.semaphore:
            for attempt in range(retry_count):
                try:
                    params = {**self.params, "page": page}
                    async with self.session.get(self.base_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()

                            # Validate response
                            if self.validate_response(data):
                                logger.debug(f"✓ Page {page} fetched successfully (attempt {attempt + 1})")
                                return data
                            else:
                                logger.warning(f"Invalid response structure for page {page}")
                        elif response.status == 429:
                            # Rate limit hit
                            wait_time = 2 ** (attempt + 2)  # Longer backoff for rate limits
                            logger.warning(f"Rate limit hit on page {page}. Waiting {wait_time}s...")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            logger.warning(f"Page {page} returned status {response.status}")

                except asyncio.TimeoutError:
                    logger.warning(f"Timeout on page {page}, attempt {attempt + 1}/{retry_count}")
                except aiohttp.ClientError as e:
                    logger.warning(f"Network error on page {page}, attempt {attempt + 1}/{retry_count}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error on page {page}, attempt {attempt + 1}/{retry_count}: {e}")

                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt
                    logger.debug(f"Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)

            logger.error(f"✗ Failed to fetch page {page} after {retry_count} attempts")
            if page not in self.failed_pages:
                self.failed_pages.append(page)
            return None

    def validate_response(self, data: Dict) -> bool:
        """Validate API response structure"""
        if not data:
            return False
        if 'products' not in data:
            return False
        if not isinstance(data['products'], list):
            return False
        return True

    def parse_product(self, product: Dict) -> Optional[Dict]:
        """Parse product data into flat structure with validation"""
        try:
            default_offer = product.get('default_offer', {})
            seller = default_offer.get('seller', {})
            main_img = product.get('main_img', {})
            category = product.get('category', {})
            ratings = product.get('ratings', {})

            # Extract product labels
            labels = product.get('product_labels', [])
            label_text = ', '.join([label.get('text', '') for label in labels if label.get('text')])

            parsed = {
                'product_id': product.get('id'),
                'name': product.get('name', '').strip(),
                'slugged_name': product.get('slugged_name', ''),
                'status': product.get('status', ''),
                'brand': product.get('brand', ''),
                'category_id': category.get('id'),
                'category_name': category.get('name', ''),

                # Pricing
                'old_price': default_offer.get('old_price', 0),
                'retail_price': default_offer.get('retail_price', 0),
                'discount_amount': default_offer.get('old_price', 0) - default_offer.get('retail_price', 0),
                'discount_percentage': round(
                    ((default_offer.get('old_price', 0) - default_offer.get('retail_price', 0)) /
                     default_offer.get('old_price', 1)) * 100, 2
                ) if default_offer.get('old_price', 0) > 0 else 0,

                # Installment
                'installment_enabled': default_offer.get('installment_enabled', False),
                'max_installment_months': default_offer.get('max_installment_months', 0),

                # Seller
                'seller_ext_id': seller.get('ext_id', ''),
                'seller_name': seller.get('marketing_name', {}).get('name', ''),
                'seller_vat_payer': seller.get('vat_payer', False),
                'seller_rating': seller.get('rating', 0),
                'seller_role': seller.get('role_name', ''),

                # Images
                'image_big': main_img.get('big', ''),
                'image_medium': main_img.get('medium', ''),
                'image_small': main_img.get('small', ''),

                # Ratings
                'rating_value': ratings.get('rating_value', 0),
                'rating_count': ratings.get('session_count', 0),

                # Other
                'product_labels': label_text,
                'min_qty': product.get('min_qty', 1),
                'preorder_available': product.get('preorder_available', False),
                'qty': default_offer.get('qty', 0),
                'offer_uuid': default_offer.get('uuid', ''),

                # Dates
                'discount_start_date': default_offer.get('discount_effective_start_date', ''),
                'discount_end_date': default_offer.get('discount_effective_end_date', ''),

                # Metadata
                'scraped_at': datetime.now().isoformat()
            }

            # Validate required fields
            if not parsed['product_id'] or not parsed['name']:
                logger.warning(f"Skipping product with missing ID or name")
                return None

            return parsed

        except Exception as e:
            logger.error(f"Error parsing product: {e}")
            return None

    async def get_total_pages(self) -> int:
        """Get total number of pages to scrape"""
        logger.info("Fetching total page count...")
        data = await self.fetch_page(1)

        if data:
            self.total_products = data.get('meta', {}).get('total', 0)
            total_pages = (self.total_products + self.params['per_page'] - 1) // self.params['per_page']
            logger.info(f"📊 Total products: {self.total_products:,}")
            logger.info(f"📄 Total pages: {total_pages:,}")
            return total_pages

        logger.error("Failed to get total page count")
        return 0

    def save_to_csv(self, products: List[Dict], filename: str, mode: str = 'a'):
        """Save products to CSV file with error handling"""
        if not products:
            return

        try:
            file_exists = Path(filename).exists() and Path(filename).stat().st_size > 0

            with open(filename, mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=products[0].keys())

                # Write header only if file is new or we're overwriting
                if not file_exists or mode == 'w':
                    writer.writeheader()

                writer.writerows(products)

            logger.info(f"💾 Saved {len(products)} products to {filename}")

        except Exception as e:
            logger.error(f"Failed to save to CSV: {e}")
            # Save to backup file
            backup_file = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                with open(backup_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=products[0].keys())
                    writer.writeheader()
                    writer.writerows(products)
                logger.info(f"Saved to backup file: {backup_file}")
            except Exception as e2:
                logger.error(f"Failed to save backup: {e2}")

    async def scrape_batch(self, pages: List[int]) -> List[Dict]:
        """Scrape a batch of pages concurrently"""
        tasks = [self.fetch_page(page) for page in pages]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_products = []
        for i, result in enumerate(results):
            page = pages[i]

            if isinstance(result, Exception):
                logger.error(f"Exception while fetching page {page}: {result}")
                continue

            if result and 'products' in result:
                for product in result['products']:
                    parsed = self.parse_product(product)
                    if parsed:
                        all_products.append(parsed)

                # Mark page as completed
                self.completed_pages.add(page)
            else:
                logger.warning(f"No products found on page {page}")

        self.scraped_count += len(all_products)
        return all_products

    async def scrape_all(self, output_file: str = 'umico_discounts.csv',
                        batch_size: int = 50, resume: bool = True):
        """Scrape all products with batching and checkpoint support"""
        logger.info("=" * 60)
        logger.info("🚀 Starting Umico Discount Scraper")
        logger.info("=" * 60)

        # Try to resume from checkpoint
        is_resuming = False
        if resume:
            is_resuming = self.load_checkpoint()

        # Get total pages if not resuming
        if not is_resuming or self.total_products == 0:
            total_pages = await self.get_total_pages()
            if total_pages == 0:
                logger.error("Could not determine total pages. Exiting.")
                return None
        else:
            total_pages = (self.total_products + self.params['per_page'] - 1) // self.params['per_page']
            logger.info(f"📄 Total pages to scrape: {total_pages:,}")

        # If not resuming, initialize CSV file
        if not is_resuming:
            Path(output_file).unlink(missing_ok=True)
            logger.info(f"📝 Starting fresh scrape")
        else:
            logger.info(f"♻️  Resuming scrape from checkpoint")

        # Scrape in batches
        start_time = datetime.now()
        save_interval = 5  # Save checkpoint every 5 batches
        batch_count = 0

        for batch_start in range(1, total_pages + 1, batch_size):
            if self.should_stop:
                logger.warning("Stopping scraper due to signal...")
                break

            batch_end = min(batch_start + batch_size, total_pages + 1)
            pages = list(range(batch_start, batch_end))

            # Filter out already completed pages
            pages_to_scrape = [p for p in pages if p not in self.completed_pages]

            if not pages_to_scrape:
                logger.debug(f"Skipping batch {batch_start}-{batch_end-1} (already completed)")
                continue

            logger.info(f"📦 Processing pages {batch_start} to {batch_end - 1} of {total_pages}")

            try:
                products = await self.scrape_batch(pages_to_scrape)

                # Save batch to CSV
                if products:
                    mode = 'w' if batch_start == 1 and not is_resuming else 'a'
                    self.save_to_csv(products, output_file, mode)

                # Progress update
                progress = len(self.completed_pages) / total_pages * 100
                elapsed = (datetime.now() - start_time).total_seconds()
                pages_per_second = len(self.completed_pages) / elapsed if elapsed > 0 else 0
                eta_seconds = (total_pages - len(self.completed_pages)) / pages_per_second if pages_per_second > 0 else 0

                logger.info(f"📊 Progress: {progress:.2f}% | "
                          f"Products: {self.scraped_count:,}/{self.total_products:,} | "
                          f"Pages: {len(self.completed_pages):,}/{total_pages:,} | "
                          f"Failed: {len(self.failed_pages)} | "
                          f"ETA: {int(eta_seconds/60)}m {int(eta_seconds%60)}s")

                batch_count += 1

                # Save checkpoint periodically
                if batch_count % save_interval == 0:
                    self.save_checkpoint()

                # Small delay between batches to avoid rate limiting
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"Error processing batch {batch_start}-{batch_end-1}: {e}")
                self.save_checkpoint()
                continue

        # Final checkpoint save
        self.save_checkpoint()

        # Retry failed pages
        if self.failed_pages and not self.should_stop:
            logger.info(f"🔄 Retrying {len(self.failed_pages)} failed pages...")
            unique_failed = list(set(self.failed_pages) - self.completed_pages)

            if unique_failed:
                retry_products = await self.scrape_batch(unique_failed)
                if retry_products:
                    self.save_to_csv(retry_products, output_file, 'a')

        # Summary
        logger.info("=" * 60)
        logger.info("✅ Scraping completed!")
        logger.info(f"📊 Total products scraped: {self.scraped_count:,}")
        logger.info(f"📄 Total pages completed: {len(self.completed_pages):,}/{total_pages:,}")
        logger.info(f"❌ Failed pages: {len(set(self.failed_pages) - self.completed_pages)}")
        logger.info(f"💾 Data saved to: {output_file}")
        logger.info(f"⏱️  Total time: {datetime.now() - start_time}")
        logger.info("=" * 60)

        # Clear checkpoint if everything succeeded
        if len(self.failed_pages) == 0 and len(self.completed_pages) == total_pages:
            self.clear_checkpoint()

        return output_file


async def main():
    """Main function to run the scraper"""
    try:
        async with UmicoScraper(max_concurrent_requests=10) as scraper:
            output_file = await scraper.scrape_all(
                output_file='umico_discounts.csv',
                batch_size=50,
                resume=True  # Enable resume from checkpoint
            )

            if scraper.failed_pages:
                failed_unique = list(set(scraper.failed_pages) - scraper.completed_pages)
                if failed_unique:
                    logger.warning(f"⚠️  {len(failed_unique)} pages failed: {failed_unique[:10]}...")
                    logger.warning("You can rerun the script to retry failed pages")

    except KeyboardInterrupt:
        logger.info("\n👋 Scraper interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
