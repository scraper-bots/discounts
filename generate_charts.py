"""
Business Analytics Chart Generator for Umico Discount Data
Generates actionable insights and visualizations for business strategy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import json
from datetime import datetime

# Set style for professional charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create charts directory
CHARTS_DIR = Path('charts')
CHARTS_DIR.mkdir(exist_ok=True)

# Configure matplotlib for better quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class BusinessAnalytics:
    """Generate business analytics charts and insights"""

    def __init__(self, csv_file='umico_discounts.csv'):
        """Load and prepare data"""
        print(f"Loading data from {csv_file}...")
        self.df = pd.read_csv(csv_file)
        self.insights = {}
        print(f"Loaded {len(self.df):,} products")

    def generate_all_charts(self):
        """Generate all business analytics charts"""
        print("\n" + "="*60)
        print("GENERATING BUSINESS ANALYTICS CHARTS")
        print("="*60 + "\n")

        # 1. Discount Distribution Analysis
        self.discount_distribution_analysis()

        # 2. Price vs Discount Strategy
        self.price_discount_strategy()

        # 3. Category Performance
        self.category_performance_analysis()

        # 4. Seller Performance Dashboard
        self.seller_performance_analysis()

        # 5. Brand Opportunity Analysis
        self.brand_opportunity_analysis()

        # 6. Customer Value Analysis
        self.customer_value_analysis()

        # 7. Competitive Positioning
        self.competitive_positioning()

        # 8. Revenue Opportunity Heatmap
        self.revenue_opportunity_heatmap()

        # 9. Market Share Analysis
        self.market_share_analysis()

        # 10. Actionable Opportunities
        self.actionable_opportunities()

        # Save insights to JSON
        self.save_insights()

        print("\n" + "="*60)
        print("CHART GENERATION COMPLETE")
        print(f"All charts saved to '{CHARTS_DIR}' folder")
        print("="*60 + "\n")

    def discount_distribution_analysis(self):
        """Analyze discount distribution patterns"""
        print("📊 Generating: Discount Distribution Analysis...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Discount Distribution Analysis - Strategic Insights',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Discount Percentage Distribution
        ax1 = axes[0, 0]
        self.df['discount_percentage'].hist(bins=50, ax=ax1, color='#2ecc71', edgecolor='black', alpha=0.7)
        ax1.axvline(self.df['discount_percentage'].median(), color='red', linestyle='--', linewidth=2,
                   label=f'Median: {self.df["discount_percentage"].median():.1f}%')
        ax1.set_xlabel('Discount Percentage (%)', fontweight='bold')
        ax1.set_ylabel('Number of Products', fontweight='bold')
        ax1.set_title('Discount % Distribution - Market Standard', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Discount Amount Distribution
        ax2 = axes[0, 1]
        discount_amount = self.df['discount_amount']
        discount_amount[discount_amount <= 500].hist(bins=50, ax=ax2, color='#3498db', edgecolor='black', alpha=0.7)
        ax2.axvline(discount_amount.median(), color='red', linestyle='--', linewidth=2,
                   label=f'Median: {discount_amount.median():.1f} AZN')
        ax2.set_xlabel('Discount Amount (AZN)', fontweight='bold')
        ax2.set_ylabel('Number of Products', fontweight='bold')
        ax2.set_title('Absolute Discount Distribution (≤500 AZN)', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Discount Segmentation
        ax3 = axes[1, 0]
        discount_segments = pd.cut(self.df['discount_percentage'],
                                   bins=[0, 20, 40, 60, 80, 100],
                                   labels=['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'])
        segment_counts = discount_segments.value_counts().sort_index()
        colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
        segment_counts.plot(kind='bar', ax=ax3, color=colors, edgecolor='black', alpha=0.8)
        ax3.set_xlabel('Discount Range', fontweight='bold')
        ax3.set_ylabel('Number of Products', fontweight='bold')
        ax3.set_title('Product Count by Discount Segment', fontweight='bold')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for i, v in enumerate(segment_counts):
            ax3.text(i, v + 50, f'{v:,}', ha='center', va='bottom', fontweight='bold')

        # 4. Price Range Analysis
        ax4 = axes[1, 1]
        price_discount = self.df.groupby(pd.cut(self.df['retail_price'],
                                               bins=[0, 50, 100, 200, 500, 2000],
                                               labels=['0-50', '50-100', '100-200', '200-500', '500+']))['discount_percentage'].mean()
        price_discount.plot(kind='bar', ax=ax4, color='#9b59b6', edgecolor='black', alpha=0.8)
        ax4.set_xlabel('Price Range (AZN)', fontweight='bold')
        ax4.set_ylabel('Average Discount %', fontweight='bold')
        ax4.set_title('Discount Strategy by Price Range', fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for i, v in enumerate(price_discount):
            ax4.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '01_discount_distribution.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['discount_distribution'] = {
            'median_discount': float(self.df['discount_percentage'].median()),
            'mean_discount': float(self.df['discount_percentage'].mean()),
            'top_segment': segment_counts.idxmax(),
            'top_segment_count': int(segment_counts.max()),
            'high_discount_products': int((self.df['discount_percentage'] > 50).sum())
        }

        print("✅ Discount Distribution Analysis complete")

    def price_discount_strategy(self):
        """Analyze price vs discount strategy"""
        print("📊 Generating: Price vs Discount Strategy...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Pricing Strategy Analysis - Revenue Optimization',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Scatter: Price vs Discount
        ax1 = axes[0, 0]
        sample = self.df[self.df['retail_price'] <= 1000].sample(min(5000, len(self.df)))
        scatter = ax1.scatter(sample['retail_price'], sample['discount_percentage'],
                            c=sample['discount_amount'], cmap='RdYlGn_r', alpha=0.5, s=30)
        ax1.set_xlabel('Retail Price (AZN)', fontweight='bold')
        ax1.set_ylabel('Discount Percentage (%)', fontweight='bold')
        ax1.set_title('Price vs Discount Strategy Map', fontweight='bold')
        plt.colorbar(scatter, ax=ax1, label='Discount Amount (AZN)')
        ax1.grid(True, alpha=0.3)

        # 2. Revenue Loss Analysis
        ax2 = axes[0, 1]
        self.df['potential_revenue_loss'] = self.df['discount_amount']
        top_loss_categories = self.df.groupby('category_name')['potential_revenue_loss'].sum().nlargest(10)
        top_loss_categories.plot(kind='barh', ax=ax2, color='#e74c3c', edgecolor='black', alpha=0.8)
        ax2.set_xlabel('Total Revenue Loss (AZN)', fontweight='bold')
        ax2.set_ylabel('Category', fontweight='bold')
        ax2.set_title('Top 10 Categories by Revenue Loss', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')

        # 3. Optimal Discount Zone
        ax3 = axes[1, 0]
        # Create bins for analysis
        self.df['discount_bin'] = pd.cut(self.df['discount_percentage'], bins=10)
        rating_by_discount = self.df[self.df['rating_count'] > 0].groupby('discount_bin')['rating_value'].mean()
        x_pos = range(len(rating_by_discount))
        bars = ax3.bar(x_pos, rating_by_discount.values, color='#3498db', edgecolor='black', alpha=0.8)

        # Highlight best performing discount range
        max_idx = rating_by_discount.argmax()
        bars[max_idx].set_color('#2ecc71')
        bars[max_idx].set_edgecolor('darkgreen')
        bars[max_idx].set_linewidth(3)

        ax3.set_xlabel('Discount Range', fontweight='bold')
        ax3.set_ylabel('Average Rating', fontweight='bold')
        ax3.set_title('Customer Satisfaction vs Discount Range', fontweight='bold')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels([f'{int(i.left)}-{int(i.right)}%' for i in rating_by_discount.index],
                           rotation=45, ha='right', fontsize=8)
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.axhline(y=rating_by_discount.mean(), color='red', linestyle='--',
                   label=f'Avg: {rating_by_discount.mean():.2f}')
        ax3.legend()

        # 4. Price Efficiency Score
        ax4 = axes[1, 1]
        # Calculate efficiency: products with high discounts but low actual savings
        self.df['price_efficiency'] = (self.df['discount_percentage'] /
                                       (self.df['discount_amount'] + 1)) * 100

        efficiency_by_seller = self.df.groupby('seller_name')['discount_percentage'].mean().nlargest(15)
        efficiency_by_seller.plot(kind='barh', ax=ax4, color='#9b59b6', edgecolor='black', alpha=0.8)
        ax4.set_xlabel('Average Discount %', fontweight='bold')
        ax4.set_ylabel('Seller', fontweight='bold')
        ax4.set_title('Top 15 Most Aggressive Discount Sellers', fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '02_price_discount_strategy.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['pricing_strategy'] = {
            'total_revenue_loss': float(self.df['discount_amount'].sum()),
            'avg_discount_amount': float(self.df['discount_amount'].mean()),
            'highest_loss_category': top_loss_categories.idxmax(),
            'highest_loss_amount': float(top_loss_categories.max())
        }

        print("✅ Price vs Discount Strategy complete")

    def category_performance_analysis(self):
        """Analyze category performance"""
        print("📊 Generating: Category Performance Analysis...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Category Performance Dashboard - Market Opportunities',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Top Categories by Product Count
        ax1 = axes[0, 0]
        top_categories = self.df['category_name'].value_counts().head(15)
        top_categories.plot(kind='barh', ax=ax1, color='#1abc9c', edgecolor='black', alpha=0.8)
        ax1.set_xlabel('Number of Products', fontweight='bold')
        ax1.set_ylabel('Category', fontweight='bold')
        ax1.set_title('Top 15 Categories by Product Volume', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')

        # 2. Category Discount Performance
        ax2 = axes[0, 1]
        category_stats = self.df.groupby('category_name').agg({
            'discount_percentage': 'mean',
            'product_id': 'count'
        }).rename(columns={'product_id': 'count'})
        category_stats = category_stats[category_stats['count'] >= 50]  # Min 50 products
        top_discount_cats = category_stats.nlargest(15, 'discount_percentage')

        top_discount_cats['discount_percentage'].plot(kind='barh', ax=ax2,
                                                      color='#e67e22', edgecolor='black', alpha=0.8)
        ax2.set_xlabel('Average Discount %', fontweight='bold')
        ax2.set_ylabel('Category', fontweight='bold')
        ax2.set_title('Categories with Highest Avg Discounts (≥50 products)', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')

        # 3. Price Distribution by Top Categories
        ax3 = axes[1, 0]
        top_5_cats = self.df['category_name'].value_counts().head(5).index
        data_to_plot = [self.df[self.df['category_name'] == cat]['retail_price'].values
                       for cat in top_5_cats]

        bp = ax3.boxplot(data_to_plot, labels=top_5_cats, patch_artist=True)
        for patch, color in zip(bp['boxes'], sns.color_palette("husl", 5)):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax3.set_ylabel('Retail Price (AZN)', fontweight='bold')
        ax3.set_xlabel('Category', fontweight='bold')
        ax3.set_title('Price Range Distribution - Top 5 Categories', fontweight='bold')
        ax3.tick_params(axis='x', rotation=45, labelsize=8)
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.set_ylim(0, 500)

        # 4. Category Market Share
        ax4 = axes[1, 1]
        category_share = self.df['category_name'].value_counts().head(10)
        colors_pie = sns.color_palette("husl", 10)
        wedges, texts, autotexts = ax4.pie(category_share.values, labels=category_share.index,
                                           autopct='%1.1f%%', colors=colors_pie, startangle=90)

        # Improve label readability
        for text in texts:
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)

        ax4.set_title('Market Share - Top 10 Categories', fontweight='bold')

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '03_category_performance.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['category_performance'] = {
            'top_category': top_categories.idxmax(),
            'top_category_count': int(top_categories.max()),
            'highest_discount_category': top_discount_cats['discount_percentage'].idxmax(),
            'highest_avg_discount': float(top_discount_cats['discount_percentage'].max())
        }

        print("✅ Category Performance Analysis complete")

    def seller_performance_analysis(self):
        """Analyze seller performance"""
        print("📊 Generating: Seller Performance Analysis...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Seller Performance Dashboard - Competitive Intelligence',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Top Sellers by Product Count
        ax1 = axes[0, 0]
        top_sellers = self.df['seller_name'].value_counts().head(15)
        top_sellers.plot(kind='barh', ax=ax1, color='#16a085', edgecolor='black', alpha=0.8)
        ax1.set_xlabel('Number of Products', fontweight='bold')
        ax1.set_ylabel('Seller', fontweight='bold')
        ax1.set_title('Top 15 Sellers by Product Volume', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')

        # 2. Seller Rating Distribution
        ax2 = axes[0, 1]
        seller_ratings = self.df.groupby('seller_name')['seller_rating'].first()
        rating_bins = pd.cut(seller_ratings, bins=[0, 80, 85, 90, 95, 100],
                           labels=['<80', '80-85', '85-90', '90-95', '95-100'])
        rating_dist = rating_bins.value_counts().sort_index()

        colors_rating = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
        rating_dist.plot(kind='bar', ax=ax2, color=colors_rating, edgecolor='black', alpha=0.8)
        ax2.set_xlabel('Rating Range', fontweight='bold')
        ax2.set_ylabel('Number of Sellers', fontweight='bold')
        ax2.set_title('Seller Quality Distribution', fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')

        # Add labels
        for i, v in enumerate(rating_dist):
            ax2.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')

        # 3. Seller Type Analysis (VAT Payers vs Non-VAT)
        ax3 = axes[1, 0]
        seller_type = self.df.groupby('seller_vat_payer').agg({
            'product_id': 'count',
            'discount_percentage': 'mean'
        })

        x = np.arange(len(seller_type))
        width = 0.35

        bars1 = ax3.bar(x - width/2, seller_type['product_id'], width,
                       label='Product Count', color='#3498db', alpha=0.8, edgecolor='black')
        ax3_twin = ax3.twinx()
        bars2 = ax3_twin.bar(x + width/2, seller_type['discount_percentage'], width,
                           label='Avg Discount %', color='#e74c3c', alpha=0.8, edgecolor='black')

        ax3.set_xlabel('Seller Type', fontweight='bold')
        ax3.set_ylabel('Product Count', fontweight='bold', color='#3498db')
        ax3_twin.set_ylabel('Average Discount %', fontweight='bold', color='#e74c3c')
        ax3.set_title('VAT vs Non-VAT Seller Comparison', fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(['Non-VAT Payer', 'VAT Payer'])
        ax3.tick_params(axis='y', labelcolor='#3498db')
        ax3_twin.tick_params(axis='y', labelcolor='#e74c3c')

        # Combined legend
        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_twin.get_legend_handles_labels()
        ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        # 4. Top Performers (High Rating + High Volume)
        ax4 = axes[1, 1]
        seller_performance = self.df.groupby('seller_name').agg({
            'product_id': 'count',
            'seller_rating': 'first'
        }).rename(columns={'product_id': 'product_count'})

        # Filter sellers with at least 20 products and rating > 90
        top_performers = seller_performance[
            (seller_performance['product_count'] >= 20) &
            (seller_performance['seller_rating'] >= 90)
        ].nlargest(15, 'product_count')

        scatter = ax4.scatter(top_performers['product_count'],
                            top_performers['seller_rating'],
                            s=top_performers['product_count']*2,
                            c=top_performers['seller_rating'],
                            cmap='RdYlGn', alpha=0.6, edgecolor='black', linewidth=1)

        ax4.set_xlabel('Product Count', fontweight='bold')
        ax4.set_ylabel('Seller Rating', fontweight='bold')
        ax4.set_title('Top Performing Sellers (≥20 products, Rating≥90)', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax4, label='Rating')

        # Annotate top 5
        for idx in top_performers.head(5).index:
            ax4.annotate(idx,
                        (top_performers.loc[idx, 'product_count'],
                         top_performers.loc[idx, 'seller_rating']),
                        fontsize=7, alpha=0.7)

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '04_seller_performance.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['seller_performance'] = {
            'top_seller': top_sellers.idxmax(),
            'top_seller_products': int(top_sellers.max()),
            'avg_seller_rating': float(self.df['seller_rating'].mean()),
            'high_quality_sellers': int((seller_ratings >= 90).sum())
        }

        print("✅ Seller Performance Analysis complete")

    def brand_opportunity_analysis(self):
        """Analyze brand opportunities"""
        print("📊 Generating: Brand Opportunity Analysis...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Brand Opportunity Analysis - Growth Potential',
                     fontsize=16, fontweight='bold', y=0.995)

        # Filter out "No Brand"
        df_brands = self.df[self.df['brand'] != 'No Brand'].copy()

        # 1. Top Brands by Presence
        ax1 = axes[0, 0]
        top_brands = df_brands['brand'].value_counts().head(20)
        top_brands.plot(kind='barh', ax=ax1, color='#8e44ad', edgecolor='black', alpha=0.8)
        ax1.set_xlabel('Number of Products', fontweight='bold')
        ax1.set_ylabel('Brand', fontweight='bold')
        ax1.set_title('Top 20 Brands by Market Presence', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')

        # 2. Brand Discount Aggressiveness
        ax2 = axes[0, 1]
        brand_stats = df_brands.groupby('brand').agg({
            'discount_percentage': 'mean',
            'product_id': 'count'
        }).rename(columns={'product_id': 'count'})

        # Brands with at least 10 products
        brand_stats_filtered = brand_stats[brand_stats['count'] >= 10]
        aggressive_brands = brand_stats_filtered.nlargest(15, 'discount_percentage')

        aggressive_brands['discount_percentage'].plot(kind='barh', ax=ax2,
                                                      color='#c0392b', edgecolor='black', alpha=0.8)
        ax2.set_xlabel('Average Discount %', fontweight='bold')
        ax2.set_ylabel('Brand', fontweight='bold')
        ax2.set_title('Most Aggressive Discount Brands (≥10 products)', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')

        # 3. Premium Brands (High Price, Lower Discount)
        ax3 = axes[1, 0]
        brand_price_stats = df_brands.groupby('brand').agg({
            'retail_price': 'mean',
            'discount_percentage': 'mean',
            'product_id': 'count'
        }).rename(columns={'product_id': 'count'})

        # Premium brands: avg price > 200, count >= 5
        premium_brands = brand_price_stats[
            (brand_price_stats['retail_price'] > 200) &
            (brand_price_stats['count'] >= 5)
        ].nlargest(15, 'retail_price')

        x = np.arange(len(premium_brands))
        width = 0.35

        ax3.barh(x - width/2, premium_brands['retail_price'], width,
                label='Avg Price (AZN)', color='#f39c12', alpha=0.8, edgecolor='black')
        ax3.barh(x + width/2, premium_brands['discount_percentage'], width,
                label='Avg Discount %', color='#3498db', alpha=0.8, edgecolor='black')

        ax3.set_yticks(x)
        ax3.set_yticklabels(premium_brands.index, fontsize=8)
        ax3.set_xlabel('Value', fontweight='bold')
        ax3.set_title('Premium Brand Positioning (Avg Price>200 AZN, ≥5 products)', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='x')

        # 4. Brand Value Score (Price * Discount)
        ax4 = axes[1, 1]
        brand_price_stats['value_score'] = (
            brand_price_stats['retail_price'] *
            brand_price_stats['discount_percentage'] / 100
        )

        value_brands = brand_price_stats[brand_price_stats['count'] >= 10].nlargest(15, 'value_score')
        value_brands['value_score'].plot(kind='barh', ax=ax4,
                                        color='#27ae60', edgecolor='black', alpha=0.8)
        ax4.set_xlabel('Value Score (Price × Discount%)', fontweight='bold')
        ax4.set_ylabel('Brand', fontweight='bold')
        ax4.set_title('Best Value Brands for Customers (≥10 products)', fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '05_brand_opportunity.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['brand_opportunities'] = {
            'top_brand': top_brands.idxmax(),
            'top_brand_count': int(top_brands.max()),
            'most_aggressive_brand': aggressive_brands['discount_percentage'].idxmax(),
            'highest_avg_discount': float(aggressive_brands['discount_percentage'].max())
        }

        print("✅ Brand Opportunity Analysis complete")

    def customer_value_analysis(self):
        """Analyze customer value propositions"""
        print("📊 Generating: Customer Value Analysis...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Customer Value Analysis - Conversion Opportunities',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Rating vs Discount Correlation
        ax1 = axes[0, 0]
        rated_products = self.df[self.df['rating_count'] > 0].copy()

        # Create bins for better visualization
        rated_products['discount_bin'] = pd.cut(rated_products['discount_percentage'],
                                                bins=[0, 20, 40, 60, 80, 100])
        rating_by_discount = rated_products.groupby('discount_bin')['rating_value'].mean()

        rating_by_discount.plot(kind='bar', ax=ax1, color='#16a085', edgecolor='black', alpha=0.8)
        ax1.set_xlabel('Discount Range (%)', fontweight='bold')
        ax1.set_ylabel('Average Rating', fontweight='bold')
        ax1.set_title('Customer Satisfaction vs Discount Level', fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.axhline(y=rated_products['rating_value'].mean(), color='red', linestyle='--',
                   label=f'Overall Avg: {rated_products["rating_value"].mean():.2f}')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for i, v in enumerate(rating_by_discount):
            ax1.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

        # 2. Installment Availability Impact
        ax2 = axes[0, 1]
        installment_stats = self.df.groupby('installment_enabled').agg({
            'product_id': 'count',
            'retail_price': 'mean',
            'discount_percentage': 'mean'
        })

        x = [0, 1]
        width = 0.25

        ax2.bar([i - width for i in x], installment_stats['product_id'], width,
               label='Product Count', color='#3498db', alpha=0.8, edgecolor='black')
        ax2_twin = ax2.twinx()
        ax2_twin.bar(x, installment_stats['retail_price'], width,
                    label='Avg Price', color='#e74c3c', alpha=0.8, edgecolor='black')
        ax2_twin.bar([i + width for i in x], installment_stats['discount_percentage'], width,
                    label='Avg Discount %', color='#2ecc71', alpha=0.8, edgecolor='black')

        ax2.set_xlabel('Installment Availability', fontweight='bold')
        ax2.set_ylabel('Product Count', fontweight='bold', color='#3498db')
        ax2_twin.set_ylabel('Price / Discount %', fontweight='bold')
        ax2.set_title('Installment Payment Impact Analysis', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(['Not Available', 'Available'])

        # Combined legend
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        # 3. Best Deals (High Discount + High Rating)
        ax3 = axes[1, 0]
        best_deals = rated_products[
            (rated_products['discount_percentage'] > 40) &
            (rated_products['rating_value'] >= 4.0) &
            (rated_products['rating_count'] >= 3)
        ]

        # Top categories with best deals
        best_deal_categories = best_deals['category_name'].value_counts().head(15)
        best_deal_categories.plot(kind='barh', ax=ax3, color='#27ae60', edgecolor='black', alpha=0.8)
        ax3.set_xlabel('Number of Best Deals', fontweight='bold')
        ax3.set_ylabel('Category', fontweight='bold')
        ax3.set_title('Categories with Most Best Deals (>40% off, Rating≥4.0)', fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')

        # 4. Value Quadrant Analysis
        ax4 = axes[1, 1]
        sample_rated = rated_products.sample(min(3000, len(rated_products)))

        scatter = ax4.scatter(sample_rated['discount_percentage'],
                            sample_rated['rating_value'],
                            c=sample_rated['retail_price'],
                            s=50, cmap='viridis', alpha=0.5, edgecolors='black', linewidth=0.5)

        # Add quadrant lines
        ax4.axvline(x=sample_rated['discount_percentage'].median(), color='red',
                   linestyle='--', alpha=0.5, label='Median Discount')
        ax4.axhline(y=sample_rated['rating_value'].median(), color='blue',
                   linestyle='--', alpha=0.5, label='Median Rating')

        ax4.set_xlabel('Discount Percentage (%)', fontweight='bold')
        ax4.set_ylabel('Rating', fontweight='bold')
        ax4.set_title('Value Quadrant Map (Color = Price)', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax4, label='Retail Price (AZN)')

        # Add quadrant labels
        ax4.text(75, 4.8, 'Premium Value', fontsize=10, fontweight='bold',
                ha='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        ax4.text(25, 4.8, 'High Quality', fontsize=10, fontweight='bold',
                ha='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '06_customer_value.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['customer_value'] = {
            'products_with_installment': int(self.df['installment_enabled'].sum()),
            'best_deals_count': len(best_deals),
            'avg_rating_rated_products': float(rated_products['rating_value'].mean()),
            'best_deal_category': best_deal_categories.idxmax() if len(best_deal_categories) > 0 else 'N/A'
        }

        print("✅ Customer Value Analysis complete")

    def competitive_positioning(self):
        """Analyze competitive positioning"""
        print("📊 Generating: Competitive Positioning...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Competitive Positioning Matrix - Strategic Planning',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Seller vs Seller Discount Competition
        ax1 = axes[0, 0]
        seller_comp = self.df.groupby('seller_name').agg({
            'product_id': 'count',
            'discount_percentage': 'mean',
            'seller_rating': 'first'
        }).rename(columns={'product_id': 'product_count'})

        # Top 30 sellers
        top_30_sellers = seller_comp.nlargest(30, 'product_count')

        scatter = ax1.scatter(top_30_sellers['discount_percentage'],
                            top_30_sellers['product_count'],
                            s=top_30_sellers['seller_rating']*3,
                            c=top_30_sellers['seller_rating'],
                            cmap='RdYlGn', alpha=0.6, edgecolor='black', linewidth=1)

        ax1.set_xlabel('Average Discount %', fontweight='bold')
        ax1.set_ylabel('Product Count', fontweight='bold')
        ax1.set_title('Seller Competitive Map (Size & Color = Rating)', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax1, label='Seller Rating')

        # 2. Price Positioning by Category
        ax2 = axes[0, 1]
        top_cats = self.df['category_name'].value_counts().head(8).index
        category_price_comp = self.df[self.df['category_name'].isin(top_cats)].groupby('category_name').agg({
            'retail_price': ['mean', 'median', 'std']
        })['retail_price']

        x = np.arange(len(category_price_comp))
        width = 0.25

        ax2.bar(x - width, category_price_comp['mean'], width,
               label='Mean', color='#3498db', alpha=0.8, edgecolor='black')
        ax2.bar(x, category_price_comp['median'], width,
               label='Median', color='#2ecc71', alpha=0.8, edgecolor='black')
        ax2.bar(x + width, category_price_comp['std'], width,
               label='Std Dev', color='#e74c3c', alpha=0.8, edgecolor='black')

        ax2.set_xlabel('Category', fontweight='bold')
        ax2.set_ylabel('Price (AZN)', fontweight='bold')
        ax2.set_title('Price Competitiveness - Top 8 Categories', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(category_price_comp.index, rotation=45, ha='right', fontsize=8)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        # 3. Market Concentration (Seller Dominance)
        ax3 = axes[1, 0]
        seller_market_share = self.df['seller_name'].value_counts()
        top_10_share = seller_market_share.head(10).sum()
        others_share = seller_market_share[10:].sum()

        concentration_data = list(seller_market_share.head(10).values) + [others_share]
        concentration_labels = list(seller_market_share.head(10).index) + ['Others']

        colors = sns.color_palette("husl", 11)
        wedges, texts, autotexts = ax3.pie(concentration_data, labels=concentration_labels,
                                           autopct='%1.1f%%', colors=colors, startangle=90)

        for text in texts:
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(7)

        ax3.set_title('Market Concentration - Seller Dominance', fontweight='bold')

        # 4. Competitive Intensity Heatmap
        ax4 = axes[1, 1]

        # Create competition matrix: categories vs avg discount
        top_10_cats = self.df['category_name'].value_counts().head(10).index
        competition_data = []
        categories_list = []

        for cat in top_10_cats:
            cat_data = self.df[self.df['category_name'] == cat]
            categories_list.append(cat[:30])  # Truncate long names

            # Calculate competition metrics
            competition_data.append([
                cat_data['discount_percentage'].mean(),
                cat_data['seller_name'].nunique(),
                cat_data['product_id'].count(),
                cat_data['retail_price'].std()
            ])

        competition_df = pd.DataFrame(competition_data,
                                     columns=['Avg Discount', 'Sellers', 'Products', 'Price Variance'],
                                     index=categories_list)

        # Normalize for heatmap
        competition_normalized = (competition_df - competition_df.min()) / (competition_df.max() - competition_df.min())

        sns.heatmap(competition_normalized, annot=True, fmt='.2f', cmap='YlOrRd',
                   ax=ax4, cbar_kws={'label': 'Intensity (Normalized)'}, linewidths=0.5)
        ax4.set_title('Competitive Intensity Matrix - Top 10 Categories', fontweight='bold')
        ax4.set_xlabel('Metric', fontweight='bold')
        ax4.set_ylabel('Category', fontweight='bold')

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '07_competitive_positioning.png', bbox_inches='tight')
        plt.close()

        # Store insights
        hhi = ((seller_market_share / seller_market_share.sum()) ** 2).sum()

        self.insights['competitive_positioning'] = {
            'market_concentration_hhi': float(hhi),
            'top_seller_share': float(seller_market_share.iloc[0] / seller_market_share.sum() * 100),
            'unique_sellers': int(self.df['seller_name'].nunique()),
            'top_10_seller_share': float(top_10_share / seller_market_share.sum() * 100)
        }

        print("✅ Competitive Positioning complete")

    def revenue_opportunity_heatmap(self):
        """Create revenue opportunity heatmap"""
        print("📊 Generating: Revenue Opportunity Heatmap...")

        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        fig.suptitle('Revenue & Growth Opportunity Analysis',
                     fontsize=16, fontweight='bold')

        # 1. Category x Seller Opportunity Matrix
        ax1 = fig.add_subplot(gs[0, :])

        # Get top categories and sellers
        top_5_cats = self.df['category_name'].value_counts().head(5).index
        top_10_sellers = self.df['seller_name'].value_counts().head(10).index

        # Create pivot table
        pivot_data = []
        for cat in top_5_cats:
            row = []
            for seller in top_10_sellers:
                count = len(self.df[(self.df['category_name'] == cat) &
                                   (self.df['seller_name'] == seller)])
                row.append(count)
            pivot_data.append(row)

        pivot_df = pd.DataFrame(pivot_data,
                               columns=[s[:20] for s in top_10_sellers],
                               index=[c[:30] for c in top_5_cats])

        sns.heatmap(pivot_df, annot=True, fmt='d', cmap='YlGnBu', ax=ax1,
                   cbar_kws={'label': 'Product Count'}, linewidths=0.5)
        ax1.set_title('Market Coverage Matrix - Top 5 Categories × Top 10 Sellers',
                     fontweight='bold', pad=20)
        ax1.set_xlabel('Seller', fontweight='bold')
        ax1.set_ylabel('Category', fontweight='bold')

        # 2. Discount vs Volume Opportunity
        ax2 = fig.add_subplot(gs[1, 0])

        # Create opportunity score: high volume + high discount = high opportunity
        category_opportunity = self.df.groupby('category_name').agg({
            'product_id': 'count',
            'discount_percentage': 'mean',
            'retail_price': 'mean'
        }).rename(columns={'product_id': 'volume'})

        category_opportunity['opportunity_score'] = (
            (category_opportunity['volume'] / category_opportunity['volume'].max()) * 0.4 +
            (category_opportunity['discount_percentage'] / 100) * 0.3 +
            (category_opportunity['retail_price'] / category_opportunity['retail_price'].max()) * 0.3
        )

        top_opportunities = category_opportunity.nlargest(15, 'opportunity_score')

        colors_opp = plt.cm.RdYlGn(top_opportunities['opportunity_score'])
        bars = ax2.barh(range(len(top_opportunities)), top_opportunities['opportunity_score'],
                       color=colors_opp, edgecolor='black', alpha=0.8)

        ax2.set_yticks(range(len(top_opportunities)))
        ax2.set_yticklabels([cat[:35] for cat in top_opportunities.index], fontsize=8)
        ax2.set_xlabel('Opportunity Score', fontweight='bold')
        ax2.set_title('Top 15 Revenue Opportunity Categories', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')

        # Add value labels
        for i, (idx, row) in enumerate(top_opportunities.iterrows()):
            ax2.text(row['opportunity_score'] + 0.01, i, f'{row["opportunity_score"]:.2f}',
                    va='center', fontsize=7, fontweight='bold')

        # 3. Growth Potential Matrix
        ax3 = fig.add_subplot(gs[1, 1])

        # Sellers with growth potential: high rating but low product count
        seller_growth = self.df.groupby('seller_name').agg({
            'product_id': 'count',
            'seller_rating': 'first',
            'discount_percentage': 'mean'
        }).rename(columns={'product_id': 'product_count'})

        # Filter: rating >= 90, products < 100
        growth_sellers = seller_growth[
            (seller_growth['seller_rating'] >= 90) &
            (seller_growth['product_count'] < 100)
        ].nlargest(15, 'seller_rating')

        x = np.arange(len(growth_sellers))
        width = 0.35

        ax3.barh(x - width/2, growth_sellers['product_count'], width,
                label='Current Products', color='#3498db', alpha=0.8, edgecolor='black')
        ax3.barh(x + width/2, growth_sellers['seller_rating'], width,
                label='Seller Rating', color='#2ecc71', alpha=0.8, edgecolor='black')

        ax3.set_yticks(x)
        ax3.set_yticklabels([s[:25] for s in growth_sellers.index], fontsize=8)
        ax3.set_xlabel('Value', fontweight='bold')
        ax3.set_title('High-Potential Sellers (Rating≥90, <100 products)', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='x')

        plt.savefig(CHARTS_DIR / '08_revenue_opportunity.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['revenue_opportunities'] = {
            'top_opportunity_category': top_opportunities.index[0],
            'opportunity_score': float(top_opportunities.iloc[0]['opportunity_score']),
            'growth_potential_sellers': int(len(growth_sellers))
        }

        print("✅ Revenue Opportunity Heatmap complete")

    def market_share_analysis(self):
        """Analyze market share dynamics"""
        print("📊 Generating: Market Share Analysis...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Market Share & Trends Analysis - Strategic Overview',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Seller Role Distribution
        ax1 = axes[0, 0]
        role_distribution = self.df['seller_role'].value_counts()

        colors_role = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        wedges, texts, autotexts = ax1.pie(role_distribution.values, labels=role_distribution.index,
                                           autopct='%1.1f%%', colors=colors_role, startangle=90,
                                           explode=[0.05] * len(role_distribution))

        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        ax1.set_title('Market Distribution by Seller Type', fontweight='bold')

        # 2. Category Diversity Index
        ax2 = axes[0, 1]

        # Calculate category diversity for top sellers
        seller_diversity = []
        for seller in self.df['seller_name'].value_counts().head(15).index:
            seller_data = self.df[self.df['seller_name'] == seller]
            category_count = seller_data['category_name'].nunique()
            product_count = len(seller_data)
            diversity_score = category_count / product_count if product_count > 0 else 0
            seller_diversity.append({
                'seller': seller,
                'categories': category_count,
                'products': product_count,
                'diversity': diversity_score
            })

        diversity_df = pd.DataFrame(seller_diversity).set_index('seller')

        x = np.arange(len(diversity_df))
        width = 0.35

        ax2.bar(x - width/2, diversity_df['categories'], width,
               label='Category Count', color='#9b59b6', alpha=0.8, edgecolor='black')
        ax2_twin = ax2.twinx()
        ax2_twin.plot(x, diversity_df['diversity'], color='#e74c3c', marker='o',
                     linewidth=2, markersize=8, label='Diversity Score')

        ax2.set_xlabel('Seller', fontweight='bold')
        ax2.set_ylabel('Category Count', fontweight='bold', color='#9b59b6')
        ax2_twin.set_ylabel('Diversity Score', fontweight='bold', color='#e74c3c')
        ax2.set_title('Seller Category Diversification - Top 15', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([s[:15] for s in diversity_df.index], rotation=45, ha='right', fontsize=7)

        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        # 3. Premium vs Budget Segments
        ax3 = axes[1, 0]

        # Define price segments
        price_segments = pd.cut(self.df['retail_price'],
                               bins=[0, 50, 100, 200, 500, float('inf')],
                               labels=['Budget\n(0-50)', 'Low-Mid\n(50-100)',
                                      'Mid\n(100-200)', 'Premium\n(200-500)', 'Luxury\n(500+)'])

        segment_stats = pd.DataFrame({
            'count': price_segments.value_counts().sort_index(),
            'avg_discount': self.df.groupby(price_segments)['discount_percentage'].mean().sort_index()
        })

        x = np.arange(len(segment_stats))
        width = 0.35

        ax3.bar(x - width/2, segment_stats['count'], width,
               label='Product Count', color='#1abc9c', alpha=0.8, edgecolor='black')
        ax3_twin = ax3.twinx()
        ax3_twin.bar(x + width/2, segment_stats['avg_discount'], width,
                    label='Avg Discount %', color='#e67e22', alpha=0.8, edgecolor='black')

        ax3.set_xlabel('Price Segment (AZN)', fontweight='bold')
        ax3.set_ylabel('Product Count', fontweight='bold', color='#1abc9c')
        ax3_twin.set_ylabel('Average Discount %', fontweight='bold', color='#e67e22')
        ax3.set_title('Market Segmentation Analysis', fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(segment_stats.index)

        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_twin.get_legend_handles_labels()
        ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        # 4. Black Friday Label Impact
        ax4 = axes[1, 1]

        # Check for Black Friday products
        self.df['has_black_friday'] = self.df['product_labels'].str.contains('Black Friday',
                                                                             case=False, na=False)

        bf_comparison = self.df.groupby('has_black_friday').agg({
            'product_id': 'count',
            'discount_percentage': 'mean',
            'retail_price': 'mean'
        }).rename(columns={'product_id': 'count'})

        x = [0, 1]
        width = 0.25

        bars1 = ax4.bar([i - width for i in x], bf_comparison['count'], width,
                       label='Product Count', color='#34495e', alpha=0.8, edgecolor='black')
        ax4_twin = ax4.twinx()
        bars2 = ax4_twin.bar(x, bf_comparison['discount_percentage'], width,
                           label='Avg Discount %', color='#e74c3c', alpha=0.8, edgecolor='black')
        bars3 = ax4_twin.bar([i + width for i in x], bf_comparison['retail_price'], width,
                           label='Avg Price', color='#3498db', alpha=0.8, edgecolor='black')

        ax4.set_xlabel('Black Friday Label', fontweight='bold')
        ax4.set_ylabel('Product Count', fontweight='bold', color='#34495e')
        ax4_twin.set_ylabel('Discount % / Price (AZN)', fontweight='bold')
        ax4.set_title('Black Friday Campaign Impact', fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(['Regular Products', 'Black Friday'])

        lines1, labels1 = ax4.get_legend_handles_labels()
        lines2, labels2 = ax4_twin.get_legend_handles_labels()
        ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=8)

        plt.tight_layout()
        plt.savefig(CHARTS_DIR / '09_market_share_trends.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['market_trends'] = {
            'black_friday_products': int(self.df['has_black_friday'].sum()),
            'bf_avg_discount': float(bf_comparison.loc[True, 'discount_percentage']) if True in bf_comparison.index else 0,
            'dominant_segment': segment_stats['count'].idxmax(),
            'premium_products': int(segment_stats.loc[segment_stats.index[-2:], 'count'].sum())
        }

        print("✅ Market Share Analysis complete")

    def actionable_opportunities(self):
        """Generate actionable business opportunities chart"""
        print("📊 Generating: Actionable Opportunities Dashboard...")

        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)

        fig.suptitle('Actionable Business Opportunities Dashboard',
                     fontsize=18, fontweight='bold')

        # 1. Underpriced Products (High quality, low price)
        ax1 = fig.add_subplot(gs[0, 0])

        rated = self.df[self.df['rating_count'] >= 3].copy()
        rated['value_score'] = rated['rating_value'] / (rated['retail_price'] + 1) * 100

        underpriced = rated.nlargest(20, 'value_score')

        ax1.barh(range(len(underpriced)), underpriced['value_score'],
                color='#27ae60', edgecolor='black', alpha=0.8)
        ax1.set_yticks(range(len(underpriced)))
        ax1.set_yticklabels([f"{name[:35]}..." if len(name) > 35 else name
                            for name in underpriced['name']], fontsize=7)
        ax1.set_xlabel('Value Score (Rating/Price×100)', fontweight='bold')
        ax1.set_title('🎯 Top 20 Best Value Products', fontweight='bold', color='#27ae60')
        ax1.grid(True, alpha=0.3, axis='x')

        # 2. Gap Analysis - Missing Products
        ax2 = fig.add_subplot(gs[0, 1])

        # Find categories with few products but high demand indicators (high avg rating)
        category_gap = self.df.groupby('category_name').agg({
            'product_id': 'count',
            'rating_value': lambda x: x[x > 0].mean() if len(x[x > 0]) > 0 else 0,
            'rating_count': 'sum'
        }).rename(columns={'product_id': 'product_count'})

        # Categories with <30 products but high engagement
        gaps = category_gap[
            (category_gap['product_count'] < 30) &
            (category_gap['rating_count'] > 5)
        ].nlargest(15, 'rating_count')

        x = np.arange(len(gaps))
        width = 0.35

        ax2.bar(x - width/2, gaps['product_count'], width,
               label='Current Products', color='#e74c3c', alpha=0.8, edgecolor='black')
        ax2.bar(x + width/2, gaps['rating_count'], width,
               label='Total Reviews', color='#3498db', alpha=0.8, edgecolor='black')

        ax2.set_xlabel('Category', fontweight='bold')
        ax2.set_ylabel('Count', fontweight='bold')
        ax2.set_title('🔍 Product Gap Opportunities (<30 products, high demand)',
                     fontweight='bold', color='#e74c3c')
        ax2.set_xticks(x)
        ax2.set_xticklabels([cat[:20] for cat in gaps.index], rotation=45, ha='right', fontsize=7)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        # 3. Price Optimization Opportunities
        ax3 = fig.add_subplot(gs[1, 0])

        # Products with very high discounts - potential for margin recovery
        high_discount_cats = self.df[self.df['discount_percentage'] > 60].groupby('category_name').agg({
            'product_id': 'count',
            'discount_percentage': 'mean',
            'discount_amount': 'sum'
        }).rename(columns={'product_id': 'count'})

        high_discount_cats = high_discount_cats[high_discount_cats['count'] >= 5].nlargest(15, 'discount_amount')

        colors_opt = plt.cm.Reds(high_discount_cats['discount_percentage'] / 100)
        ax3.barh(range(len(high_discount_cats)), high_discount_cats['discount_amount'],
                color=colors_opt, edgecolor='black', alpha=0.8)

        ax3.set_yticks(range(len(high_discount_cats)))
        ax3.set_yticklabels([cat[:35] for cat in high_discount_cats.index], fontsize=7)
        ax3.set_xlabel('Total Potential Revenue Recovery (AZN)', fontweight='bold')
        ax3.set_title('💰 Price Optimization Targets (>60% discount categories)',
                     fontweight='bold', color='#c0392b')
        ax3.grid(True, alpha=0.3, axis='x')

        # 4. Seller Partnership Opportunities
        ax4 = fig.add_subplot(gs[1, 1])

        # High-rated sellers with limited product range
        seller_partnership = self.df.groupby('seller_name').agg({
            'product_id': 'count',
            'seller_rating': 'first',
            'category_name': 'nunique'
        }).rename(columns={'product_id': 'products', 'category_name': 'categories'})

        partnership_targets = seller_partnership[
            (seller_partnership['seller_rating'] >= 92) &
            (seller_partnership['products'] >= 10) &
            (seller_partnership['products'] <= 50)
        ].nlargest(15, 'seller_rating')

        scatter = ax4.scatter(partnership_targets['products'],
                            partnership_targets['categories'],
                            s=partnership_targets['seller_rating']*5,
                            c=partnership_targets['seller_rating'],
                            cmap='Greens', alpha=0.6, edgecolor='black', linewidth=1.5)

        ax4.set_xlabel('Product Count', fontweight='bold')
        ax4.set_ylabel('Category Diversity', fontweight='bold')
        ax4.set_title('🤝 Seller Expansion Opportunities (Rating≥92, 10-50 products)',
                     fontweight='bold', color='#27ae60')
        ax4.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax4, label='Seller Rating')

        # Annotate top 3
        for idx in partnership_targets.head(3).index:
            ax4.annotate(idx[:15],
                        (partnership_targets.loc[idx, 'products'],
                         partnership_targets.loc[idx, 'categories']),
                        fontsize=7, fontweight='bold')

        # 5. Cross-sell Opportunities
        ax5 = fig.add_subplot(gs[2, 0])

        # Products frequently bought categories (based on seller overlap)
        top_sellers = self.df['seller_name'].value_counts().head(10).index
        crosssell_data = []

        for seller in top_sellers[:5]:
            seller_cats = self.df[self.df['seller_name'] == seller]['category_name'].value_counts().head(3)
            for cat, count in seller_cats.items():
                crosssell_data.append({
                    'seller': seller[:20],
                    'category': cat[:25],
                    'count': count
                })

        if crosssell_data:
            crosssell_df = pd.DataFrame(crosssell_data)
            pivot = crosssell_df.pivot_table(index='category', columns='seller',
                                            values='count', fill_value=0)

            sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGn', ax=ax5,
                       cbar_kws={'label': 'Product Count'}, linewidths=0.5)
            ax5.set_title('🔄 Cross-Sell Patterns - Top Sellers×Categories',
                         fontweight='bold', color='#16a085')
            ax5.set_xlabel('Seller', fontweight='bold')
            ax5.set_ylabel('Category', fontweight='bold')

        # 6. Key Metrics Summary
        ax6 = fig.add_subplot(gs[2, 1])
        ax6.axis('off')

        # Calculate key opportunity metrics
        total_revenue_at_risk = self.df['discount_amount'].sum()
        avg_margin_opportunity = self.df[self.df['discount_percentage'] > 50]['discount_percentage'].mean()
        high_value_products = len(underpriced)
        gap_categories = len(gaps)

        summary_text = f"""
        📊 KEY OPPORTUNITY METRICS

        💵 Total Revenue at Risk: {total_revenue_at_risk:,.0f} AZN
           (from current discounts)

        📈 Avg Margin Recovery Potential: {avg_margin_opportunity:.1f}%
           (from products with >50% discount)

        🎯 High-Value Products Identified: {high_value_products}
           (best rating-to-price ratio)

        🔍 Product Gap Categories: {gap_categories}
           (high demand, low supply)

        🤝 Partnership Targets: {len(partnership_targets)}
           (high-rated sellers, growth potential)

        💰 Price Optimization Targets: {len(high_discount_cats)} categories
           (excessive discount opportunities)

        ⭐ Recommended Actions:
        1. Review pricing strategy for high-discount categories
        2. Expand partnerships with top-rated sellers
        3. Fill product gaps in high-demand categories
        4. Optimize discount levels while maintaining conversion
        5. Focus on cross-selling within top seller portfolios
        """

        ax6.text(0.1, 0.95, summary_text, transform=ax6.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        plt.savefig(CHARTS_DIR / '10_actionable_opportunities.png', bbox_inches='tight')
        plt.close()

        # Store insights
        self.insights['actionable_opportunities'] = {
            'total_revenue_at_risk': float(total_revenue_at_risk),
            'margin_recovery_potential': float(avg_margin_opportunity),
            'high_value_products': int(high_value_products),
            'gap_categories': int(gap_categories),
            'partnership_targets': int(len(partnership_targets)),
            'price_optimization_categories': int(len(high_discount_cats))
        }

        print("✅ Actionable Opportunities Dashboard complete")

    def save_insights(self):
        """Save all insights to JSON file"""
        insights_file = 'business_insights.json'

        # Add summary
        self.insights['summary'] = {
            'total_products': int(len(self.df)),
            'total_categories': int(self.df['category_name'].nunique()),
            'total_sellers': int(self.df['seller_name'].nunique()),
            'total_brands': int(self.df['brand'].nunique()),
            'avg_discount_percentage': float(self.df['discount_percentage'].mean()),
            'total_discount_amount': float(self.df['discount_amount'].sum()),
            'products_with_ratings': int((self.df['rating_count'] > 0).sum()),
            'avg_rating': float(self.df[self.df['rating_count'] > 0]['rating_value'].mean()),
            'generated_at': datetime.now().isoformat()
        }

        with open(insights_file, 'w') as f:
            json.dump(self.insights, f, indent=2)

        print(f"\n💾 Business insights saved to '{insights_file}'")


def main():
    """Main execution"""
    analytics = BusinessAnalytics('umico_discounts.csv')
    analytics.generate_all_charts()

    print("\n" + "="*60)
    print("SUCCESS! All charts and insights generated")
    print("="*60)
    print(f"\nCheck the '{CHARTS_DIR}' folder for all visualizations")
    print("Check 'business_insights.json' for detailed metrics")
    print("\nCharts generated:")
    for i, chart in enumerate(sorted(CHARTS_DIR.glob('*.png')), 1):
        print(f"  {i}. {chart.name}")


if __name__ == "__main__":
    main()
