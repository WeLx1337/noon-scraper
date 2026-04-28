# 🔍 Noon Scraper

A fast, modular Python scraper for [Noon.com](https://www.noon.com) — extracts product names, prices, images, links, and Express status across Saudi Arabia, UAE, and Egypt. Ships with a developer CLI and a clean Flask web UI.

## 🚀 Live Demo

**[noon-scraper.onrender.com](https://noon-scraper.onrender.com)**

> ⚠️ Hosted on Render's free tier — first load may take ~30 seconds to spin up. For faster results, use the CLI locally.

---

## ✨ Features

- 🌍 Supports **Saudi Arabia**, **UAE**, and **Egypt** domains
- 🖼️ Extracts **name, price, image, link, and Express badge**
- 📄 Multi-page scraping (up to 8 pages / ~400 products)
- 📥 Export to **JSON or CSV** via CLI or Web UI
- 🤖 **MCP Server** for LM Studio / Claude Desktop integration
- 🧱 Clean modular architecture — scraper, CLI, and Flask are fully separated

---

## 💻 CLI (Recommended)

The CLI is the fastest and most flexible way to use the scraper.

```bash
# Basic search (outputs JSON to terminal)
python cli.py -q "laptop"

# Save 4 pages of UAE results as CSV
python cli.py -q "iPhone 15" -p 4 -c uae -o csv -f results.csv

# Saudi Arabia, 2 pages, JSON file
python cli.py -q "rtx 5070" -p 2 -c saudi -o json -f rtx.json
```

### CLI Options

| Flag | Long | Description | Default |
|------|------|-------------|---------|
| `-q` | `--query` | Search term | *(required)* |
| `-p` | `--pages` | Pages to scrape | `2` |
| `-c` | `--country` | `saudi`, `uae`, or `egypt` | `saudi` |
| `-o` | `--output` | `json` or `csv` | `json` |
| `-f` | `--file` | Output filename | stdout |

---

## 🤖 MCP Server (LM Studio / Claude Desktop)

This project includes an MCP server that exposes the scraper as an AI tool, letting any MCP-compatible LLM search Noon products on demand.

```bash
python noon_mcp_server.py
```

Then add it to your LM Studio or Claude Desktop MCP config. The tool is called `search_noon_products` and accepts `query`, `country`, and `pages` arguments.

---

## 📦 Installation

```bash
git clone https://github.com/WeLx1337/noon-scraper.git
cd noon-scraper
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🌐 Web UI (Local)

Prefer a visual interface? Run the Flask app locally for full speed without cold starts.

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

- Search any product across KSA / UAE / Egypt
- Sort and filter results in real time
- Download results as a CSV file

---

## ☁️ Self-Hosting

The repo is pre-configured for **Render**, **Railway**, and **Heroku**.

Includes a `Procfile` using `gunicorn` and auto-detects the `PORT` environment variable.

```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

No additional configuration needed — just connect your repo and deploy.

---

## 🗂️ Project Structure

```
noon-scraper/
├── scraper.py          # Core scraping logic (curl-cffi + BeautifulSoup)
├── app.py              # Flask web app
├── cli.py              # Developer CLI
├── noon_mcp_server.py  # MCP server for AI tool use
├── templates/
│   └── index.html      # Web UI
├── Procfile            # For Render / Heroku deployment
└── requirements.txt
```

---

## 🛠️ Tech Stack

- **[curl-cffi](https://github.com/yifeikong/curl-cffi)** — browser impersonation to bypass bot detection
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** — HTML parsing
- **[Flask](https://flask.palletsprojects.com/)** — lightweight web server
- **[FastMCP](https://github.com/jlowin/fastmcp)** — MCP server framework

---

## ⚠️ Disclaimer

This project is built for educational purposes. Scraping websites may violate their Terms of Service. Use responsibly and check Noon's ToS before using in production.

---

## 📄 License

MIT © [Abdullah](https://github.com/WeLx1337/)
