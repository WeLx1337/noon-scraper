A modular Python-based scraper designed to extract regional product data from Noon.com. This project demonstrates clean modular logic, featuring a robust CLI for developers and a lightweight Flask web interface for quick data exports.

## 📖 Features
- **Scraping:** Supports KSA, UAE, and Egypt domains.
- **Data:** Extracts names, prices, links, images, and "Express" status.
- **Export:** Save data as JSON or CSV via CLI or Web.
- **Clean Code:** Separated logic for scraper, CLI# Noon Scraper

A lightweight student project demonstrating web scraping, a Flask UI, and a developer-focused CLI tool.

## 🚀 Live Demo
**[Noon Scraper](https://noon-scraper.onrender.com)**  
*Note: The live demo uses free hosting, so it is significantly slower than running the script locally. You can scrape products and download CSV results directly from the web interface.*

## 💻 CLI Usage (Recommended)
The CLI is the most efficient way to use the scraper.
```bash
# Basic search
python cli.py -q "laptop"

# Save 4 pages of UAE results to a CSV file
python cli.py -q "iPhone 15" -p 4 -c uae -o csv -f results.csv

# Options:
# -q, --query    Search term (Required)
# -p, --pages    Pages to scrape (Default: 2, Max: 8)
# -c, --country  saudi, uae, or egypt (Default: saudi)
# -o, --output   json or csv (Default: json)
# -f, --file     Filename to save output
```

## 🛠️ Setup & Local Run
1. **Install:**
   ```bash
   git clone <repository-url>
   cd noon_web
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Web UI Locally:**
   ```bash
   python app.py
   ```
   Access at `http://127.0.0.1:5000`.

## ☁️ Hosting Ready
This repo is pre-configured for **Render**, Heroku, or Railway.
- Includes a `Procfile` and `gunicorn` for production.
- Detects `PORT` from environment variables automatically.

## 📖 Features
- **Scraping:** Supports KSA, UAE, and Egypt domains.
- **Data:** Extracts names, prices, links, images, and "Express" status.
- **Export:** Save data as JSON or CSV via CLI or Web.
- **Clean Code:** Separated logic for scraper, CLI, and Flask.
