# Umico Discount Products Scraper

Asynchronous web scraper for extracting discount product data from Umico marketplace using Python asyncio and aiohttp.

## Features

- **Async/Concurrent Scraping**: Uses asyncio and aiohttp for fast, non-blocking HTTP requests
- **Crash-Proof Design**: Checkpoint/resume functionality - automatically continues from where it left off
- **Batch Processing**: Scrapes pages in batches to manage memory and save progress incrementally
- **Enhanced Error Handling**: 5-attempt retry logic with exponential backoff for failed requests
- **Data Integrity**: Progressive CSV saving ensures no data loss even if scraper stops
- **Graceful Shutdown**: Signal handling (Ctrl+C) saves checkpoint before exiting
- **Rate Limiting**: Semaphore-based concurrency control with 429 status handling
- **Data Validation**: Validates responses and parsed products to ensure data quality
- **Comprehensive Logging**: Detailed logs saved to file and console with emoji indicators
- **Progress Tracking**: Real-time progress with ETA, products/pages count, and completion percentage
- **Backup System**: Automatic backup files if primary save fails

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python scraper.py
```

This will:
- Scrape all discount products from Umico
- Save data to `umico_discounts.csv`
- Create a log file `scraper.log`
- Process 50 pages per batch
- Use 10 concurrent requests

### Customization

You can customize the scraper by modifying the `main()` function in `scraper.py`:

```python
async with UmicoScraper(max_concurrent_requests=10) as scraper:
    output_file = await scraper.scrape_all(
        output_file='umico_discounts.csv',  # Output filename
        batch_size=50                        # Pages per batch
    )
```

**Parameters:**
- `max_concurrent_requests`: Number of simultaneous HTTP requests (default: 10)
- `output_file`: CSV output filename (default: 'umico_discounts.csv')
- `batch_size`: Number of pages to process before saving (default: 50)

## Output Data

The scraper extracts and saves the following fields:

### Product Information
- `product_id`: Unique product identifier
- `name`: Product name
- `slugged_name`: URL-friendly product name
- `status`: Product status (active/inactive)
- `brand`: Product brand

### Category
- `category_id`: Category identifier
- `category_name`: Category name

### Pricing
- `old_price`: Original price before discount
- `retail_price`: Current discounted price
- `discount_amount`: Absolute discount amount
- `discount_percentage`: Discount percentage

### Installment
- `installment_enabled`: Whether installment is available
- `max_installment_months`: Maximum installment period

### Seller Information
- `seller_ext_id`: Seller identifier
- `seller_name`: Seller/store name
- `seller_vat_payer`: Whether seller pays VAT
- `seller_rating`: Seller rating (0-100)
- `seller_role`: Seller role (FBU/3P)

### Images
- `image_big`: Large image URL (1680px)
- `image_medium`: Medium image URL (840px)
- `image_small`: Small image URL (280px)

### Ratings
- `rating_value`: Product rating (0-5)
- `rating_count`: Number of ratings

### Other
- `product_labels`: Product labels (e.g., "Black Friday")
- `min_qty`: Minimum order quantity
- `preorder_available`: Whether preorder is available
- `qty`: Available quantity
- `offer_uuid`: Unique offer identifier
- `discount_start_date`: Discount start date
- `discount_end_date`: Discount end date
- `scraped_at`: Timestamp when data was scraped

## Crash-Proof & Resume Features

### Checkpoint System
The scraper automatically saves progress every 5 batches to `scraper_checkpoint.json`. If the scraper crashes, stops, or you interrupt it (Ctrl+C), simply rerun the script and it will resume from where it left off.

### How It Works
1. **Automatic Checkpoints**: Progress is saved every 5 batches
2. **Graceful Shutdown**: Pressing Ctrl+C saves checkpoint before exiting
3. **Auto-Resume**: On restart, automatically detects and loads checkpoint
4. **Skip Completed**: Only scrapes pages that haven't been completed yet
5. **Failed Page Retry**: Tracks and retries failed pages at the end

### Recovery Examples

**Scenario 1: Crash during scraping**
```bash
# First run - crashes at 50%
python scraper.py
# Progress: 50% (45000/90000 products)
# ERROR: Connection lost...

# Second run - resumes automatically
python scraper.py
# ♻️ Resuming scrape from checkpoint
# Checkpoint loaded: 1875 pages already completed
# Continuing from page 1876...
```

**Scenario 2: Intentional stop**
```bash
# Stop with Ctrl+C
python scraper.py
# ^C
# ⚠️ Received signal 2. Initiating graceful shutdown...
# Checkpoint saved: 1000 pages completed

# Resume later
python scraper.py
# ♻️ Resuming scrape from checkpoint
```

**Scenario 3: Fresh start**
```bash
# Delete checkpoint to start fresh
rm scraper_checkpoint.json
python scraper.py
```

## Performance

- **Expected Runtime**: ~10-15 minutes for 90,000 products (~3,800 pages)
- **Memory Usage**: ~200-500 MB (depending on batch size)
- **Request Rate**: ~10 requests/second (configurable)
- **Handles**: 3,800+ pages without data loss

## Error Handling

The scraper includes robust error handling:

1. **Retry Logic**: Each failed request is retried up to 3 times with exponential backoff
2. **Failed Pages Tracking**: Pages that fail after all retries are tracked and retried at the end
3. **Progressive Saving**: Data is saved after each batch to prevent data loss
4. **Timeout Handling**: 30-second timeout per request

## Logging

Logs are written to both console and `scraper.log` file with emoji indicators for easy scanning:

- **INFO**: Progress updates, successful requests (🚀 📊 💾 📄 etc.)
- **WARNING**: Retries, non-200 status codes, rate limits (⚠️)
- **ERROR**: Failed requests, parsing errors (❌ ✗)

Example log output:
```
============================================================
🚀 Starting Umico Discount Scraper
============================================================
2025-11-27 12:00:00 - INFO - Fetching total page count...
2025-11-27 12:00:01 - INFO - 📊 Total products: 90,000
2025-11-27 12:00:01 - INFO - 📄 Total pages: 3,750
2025-11-27 12:00:01 - INFO - 📝 Starting fresh scrape
2025-11-27 12:00:05 - INFO - 📦 Processing pages 1 to 50 of 3750
2025-11-27 12:00:15 - INFO - 💾 Saved 1,200 products to umico_discounts.csv
2025-11-27 12:00:15 - INFO - 📊 Progress: 1.33% | Products: 1,200/90,000 | Pages: 50/3,750 | Failed: 0 | ETA: 12m 30s
2025-11-27 12:00:15 - INFO - Checkpoint saved: 50 pages completed
```

## Data Analysis

The output CSV is ready for analysis with:
- **Pandas**: `pd.read_csv('umico_discounts.csv')`
- **Excel**: Can be opened directly in Excel/Google Sheets
- **SQL**: Can be imported into databases for analysis

Example analysis queries:
- Products with highest discount percentages
- Most popular sellers
- Price distribution by category
- Installment availability trends

## Troubleshooting

### Scraper is too slow
- Increase `max_concurrent_requests` (but be careful not to get blocked)
- Increase `batch_size` to save less frequently

### Getting timeout errors
- Decrease `max_concurrent_requests` to reduce load
- Check your internet connection

### Missing products
- Check `scraper.log` for failed pages
- Rerun the scraper (it will append to existing CSV)
- Failed pages are automatically retried at the end

## Notes

- The scraper respects the target server by implementing rate limiting
- Data is saved progressively to prevent loss
- All timestamps are in ISO format
- CSV uses UTF-8 encoding for proper character support

## License

This scraper is for educational and analysis purposes only.
