# Noon Scraper

This is a small Noon.com scraper built as a simple student project. It is not a big product—just a learning repo showing how to scrape a website, build a little Flask UI, and add a command-line tool.

## What it does

- Scrapes product listings from Noon by search query
- Supports Saudi Arabia, UAE, and Egypt domains
- Returns product name, price, link, image URL, and express delivery status
- Includes a browser UI and a developer CLI
- Lets you export results as CSV

## Project structure

```
noon_web/
├── scraper.py          # Core scraping logic
├── app.py              # Flask web app and routes
├── cli.py              # Developer CLI interface
├── requirements.txt    # Python dependencies
├── Procfile           # Hosting helper for tools like Heroku/Render
├── .gitignore          # Ignored files in Git
└── templates/
    └── index.html      # Web UI template
```

## Setup and install

1. Clone the repo:
   ```bash
git clone <repository-url>
cd noon_web
```

2. Create a Python virtual environment:
   ```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS / Linux
source .venv/bin/activate
```

3. Install the requirements:
   ```bash
pip install -r requirements.txt
```

## Run the web app locally

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Hosting ready

This project is ready for Python-friendly hosts like Heroku, Render, Railway, or Replit.

- The app uses `PORT` from the environment when available
- `requirements.txt` includes `gunicorn`
- `Procfile` is provided for quick deployment

### Run with Gunicorn

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

## CLI usage

For developers, the CLI is the easiest way to scrape without the web UI.

```bash
python cli.py --query "laptop" --pages 3 --country saudi --output json
```

### CLI options

- `--query` or `-q` — search term (required)
- `--pages` or `-p` — pages to scrape (default: 2, max: 8)
- `--country` or `-c` — `saudi`, `uae`, or `egypt` (default: `saudi`)
- `--output` or `-o` — `json` or `csv` (default: `json`)
- `--file` or `-f` — save output to a file (optional)

### CLI examples

```bash
# Simple search
python cli.py -q "wireless headphones"

# Save CSV results
python cli.py -q "iPhone 15" -p 4 -c uae -o csv -f noon_laptops.csv

# Save JSON to a file
python cli.py -q "gaming mouse" -o json -f results.json

# Get help
python cli.py --help
```

## Using the scraper in Python

If you want to use the scraper in your own script:

```python
from scraper import scrape_noon

products = scrape_noon(query="laptop", pages=2, country="saudi")
for product in products:
    print(product)
```

## Notes for beginners

This repo is meant to be a beginner project, so it is okay that it is small. It shows:

- a separate scraper module
- a Flask UI
- a CLI interface
- how to organize a simple Python project

If this is your first repo, that is great! Keep it simple and clear.

## License

MIT License
