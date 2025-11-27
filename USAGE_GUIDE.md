# Complete Usage Guide - Umico Analytics Project

## Quick Start (3 Steps)

### Step 1: Scrape the Data
```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper (auto-resumes if interrupted)
python scraper.py
```

**Output:** `umico_discounts.csv` with 90,000+ products

**Duration:** ~10-15 minutes for full scrape

**Features:**
- ✅ Crash-proof with checkpoint/resume
- ✅ Auto-retry failed pages
- ✅ Progress tracking with ETA
- ✅ Detailed logging

---

### Step 2: Generate Analytics Charts
```bash
# Generate all 10 business analytics charts
python generate_charts.py
```

**Output:**
- 10 high-resolution charts in `/charts` folder
- `business_insights.json` with key metrics

**Duration:** ~2-3 minutes

**Charts Generated:**
1. Discount Distribution Analysis
2. Price & Discount Strategy
3. Category Performance
4. Seller Performance
5. Brand Opportunities
6. Customer Value Analysis
7. Competitive Positioning
8. Revenue Opportunities
9. Market Share & Trends
10. Actionable Opportunities

---

### Step 3: View the Presentation
```bash
# Open the business analytics report
open BUSINESS_ANALYTICS.md
```

**Content:**
- ✅ Executive Summary with key findings
- ✅ 10 detailed analysis sections with embedded charts
- ✅ Actionable business recommendations
- ✅ Strategic roadmap with ROI projections
- ✅ 90-day action plan
- ✅ Risk mitigation strategies

---

## Project Structure

```
discounts/
├── scraper.py                    # Async web scraper (crash-proof)
├── generate_charts.py            # Business analytics chart generator
├── analyze_example.py            # Additional data analysis examples
├── umico_discounts.csv           # Scraped data (90,000+ products)
├── scraper_checkpoint.json       # Resume checkpoint (auto-generated)
├── scraper.log                   # Scraper execution logs
├── business_insights.json        # Key metrics and insights
├── requirements.txt              # Python dependencies
├── README.md                     # Original scraper documentation
├── BUSINESS_ANALYTICS.md         # 📊 PRESENTATION DOCUMENT (MAIN OUTPUT)
├── USAGE_GUIDE.md               # This file
└── charts/                       # Generated visualizations
    ├── 01_discount_distribution.png
    ├── 02_price_discount_strategy.png
    ├── 03_category_performance.png
    ├── 04_seller_performance.png
    ├── 05_brand_opportunity.png
    ├── 06_customer_value.png
    ├── 07_competitive_positioning.png
    ├── 08_revenue_opportunity.png
    ├── 09_market_share_trends.png
    └── 10_actionable_opportunities.png
```

---

## Common Workflows

### Workflow 1: Fresh Start
```bash
# Clean slate - scrape and analyze everything
rm umico_discounts.csv scraper_checkpoint.json  # Optional: remove old data
python scraper.py                               # Scrape fresh data
python generate_charts.py                       # Generate charts
open BUSINESS_ANALYTICS.md                      # View presentation
```

### Workflow 2: Resume Interrupted Scrape
```bash
# If scraper was interrupted, just rerun
python scraper.py  # Automatically resumes from checkpoint
```

### Workflow 3: Re-generate Charts Only
```bash
# If you have the CSV but want new charts
python generate_charts.py  # Uses existing umico_discounts.csv
```

### Workflow 4: Custom Analysis
```bash
# Use the example analysis script
python analyze_example.py  # Generates custom insights
```

---

## Customization Options

### Adjust Scraper Settings

Edit `scraper.py`:

```python
# In the main() function at the bottom:
async with UmicoScraper(max_concurrent_requests=10) as scraper:  # Change concurrency
    output_file = await scraper.scrape_all(
        output_file='umico_discounts.csv',  # Change output filename
        batch_size=50,                       # Change batch size
        resume=True                          # Enable/disable resume
    )
```

### Adjust Chart Generation

Edit `generate_charts.py`:

```python
# In the __init__ method:
def __init__(self, csv_file='umico_discounts.csv'):  # Change input file

# In main():
analytics = BusinessAnalytics('custom_data.csv')  # Use custom CSV
```

### Chart Quality Settings

In `generate_charts.py` at the top:

```python
# Configure matplotlib for better quality
plt.rcParams['figure.dpi'] = 300        # Change resolution (default: 300)
plt.rcParams['savefig.dpi'] = 300       # Change save quality
plt.rcParams['figure.figsize'] = (12, 6) # Change default size
plt.rcParams['font.size'] = 10          # Change font size
```

---

## Troubleshooting

### Problem: Scraper fails to start
**Solution:** Check your internet connection and API availability
```bash
# Test API manually
curl "https://mp-catalog.umico.az/api/v1/products?page=1&per_page=24"
```

### Problem: Charts not generating
**Solution:** Ensure all dependencies are installed
```bash
pip install --upgrade pandas matplotlib seaborn numpy
```

### Problem: Out of memory during scraping
**Solution:** Reduce batch size
```python
# In scraper.py main() function:
batch_size=25  # Reduce from 50 to 25
```

### Problem: Charts look blurry
**Solution:** Increase DPI in generate_charts.py
```python
plt.rcParams['figure.dpi'] = 600  # Increase from 300
plt.rcParams['savefig.dpi'] = 600
```

---

## Performance Benchmarks

**On a typical laptop:**

| Operation | Duration | Output Size |
|-----------|----------|-------------|
| Scraping 3,750 pages | 10-15 min | ~25 MB CSV |
| Generating 10 charts | 2-3 min | ~15 MB PNG files |
| Loading CSV in Pandas | 3-5 sec | ~200 MB RAM |
| Full workflow | 15-20 min | ~40 MB total |

---

## Tips & Best Practices

### For Scraping:
✅ Run scraper during off-peak hours for better speed
✅ Keep checkpoint file until scraping completes
✅ Monitor `scraper.log` for any issues
✅ Don't modify CSV while scraper is running

### For Chart Generation:
✅ Close other memory-intensive applications
✅ Run in a terminal to see progress messages
✅ Check `business_insights.json` for raw metrics
✅ Charts are saved in PNG format (editable in design tools)

### For Presentations:
✅ View `BUSINESS_ANALYTICS.md` in a Markdown viewer for best formatting
✅ Export to PDF for sharing (use tools like Typora, Pandoc)
✅ Charts can be individually extracted from `/charts` folder
✅ Customize insights in the MD file for your audience

---

## Data Fields Reference

The CSV contains these key fields:

**Product Info:**
- product_id, name, brand, category_name, slugged_name

**Pricing:**
- old_price, retail_price, discount_amount, discount_percentage

**Seller:**
- seller_name, seller_rating, seller_vat_payer, seller_role

**Ratings:**
- rating_value, rating_count

**Other:**
- installment_enabled, max_installment_months
- image_big, image_medium, image_small
- product_labels, scraped_at

---

## Export Options

### Export to Excel
```python
import pandas as pd
df = pd.read_csv('umico_discounts.csv')
df.to_excel('umico_discounts.xlsx', index=False)
```

### Export to Database
```python
import pandas as pd
import sqlite3

df = pd.read_csv('umico_discounts.csv')
conn = sqlite3.connect('umico.db')
df.to_sql('products', conn, if_exists='replace', index=False)
```

### Export Charts to PDF
```bash
# Using markdown to PDF converter
pandoc BUSINESS_ANALYTICS.md -o BUSINESS_ANALYTICS.pdf --pdf-engine=xelatex
```

---

## Advanced Usage

### Combine with SQL for Analysis
```bash
# Load data into SQLite
sqlite3 umico.db < import_script.sql

# Query examples
sqlite3 umico.db "SELECT category_name, AVG(discount_percentage)
                  FROM products
                  GROUP BY category_name
                  ORDER BY AVG(discount_percentage) DESC
                  LIMIT 10;"
```

### Schedule Regular Scraping
```bash
# Add to crontab for daily scraping
0 2 * * * cd /path/to/discounts && python scraper.py >> cron.log 2>&1
```

### Integrate with BI Tools
- Export CSV to Tableau, Power BI, Looker, etc.
- Use `business_insights.json` for automated dashboards
- Connect directly to database for real-time queries

---

## Support & Resources

**Documentation:**
- `README.md` - Scraper technical documentation
- `BUSINESS_ANALYTICS.md` - Business presentation
- `USAGE_GUIDE.md` - This file

**Code:**
- `scraper.py` - Well-commented scraper code
- `generate_charts.py` - Chart generation with insights
- `analyze_example.py` - Additional analysis examples

**Generated Files:**
- `business_insights.json` - Machine-readable insights
- `scraper.log` - Execution logs for debugging
- Charts (PNG) - High-resolution visualizations

---

## Next Steps

1. ✅ Run the scraper to get fresh data
2. ✅ Generate charts for visual insights
3. ✅ Review `BUSINESS_ANALYTICS.md` for strategy
4. ✅ Customize analysis for your specific needs
5. ✅ Present findings to stakeholders
6. ✅ Implement recommended actions

---

**Questions or Issues?**

Check the logs, review the code comments, or modify the scripts for your specific needs. All code is designed to be readable and customizable.

**Happy Analyzing! 📊**
