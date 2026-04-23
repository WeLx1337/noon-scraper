#!/usr/bin/env python3
"""
Noon Scraper CLI - Developer Tool

This is a command-line interface for developers to scrape Noon.com products.
It provides programmatic access to the scraper without the web UI.

Usage:
    python cli.py --query "laptop" --pages 3 --country saudi --output json

Options:
    --query: Search query (required)
    --pages: Number of pages to scrape (default: 2)
    --country: Country domain - saudi, uae, egypt (default: saudi)
    --output: Output format - json or csv (default: json)
    --file: Output file path (optional, prints to stdout if not specified)
"""

import argparse
import json
import csv
import io
import sys
from scraper import scrape_noon

def main():
    parser = argparse.ArgumentParser(
        description="Scrape Noon.com products via command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--query", "-q",
        required=True,
        help="Search query for products"
    )

    parser.add_argument(
        "--pages", "-p",
        type=int,
        default=2,
        help="Number of pages to scrape (default: 2)"
    )

    parser.add_argument(
        "--country", "-c",
        choices=["saudi", "uae", "egypt"],
        default="saudi",
        help="Country domain (default: saudi)"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )

    parser.add_argument(
        "--file", "-f",
        help="Output file path (prints to stdout if not specified)"
    )

    args = parser.parse_args()

    # Progress callback function
    def progress_callback(message):
        print(f"[INFO] {message}", file=sys.stderr)

    # Scrape the products
    print(f"Starting scrape for '{args.query}' from {args.country} domain ({args.pages} pages)...", file=sys.stderr)
    products = scrape_noon(args.query, args.pages, args.country, progress_callback=progress_callback)
    print(f"✓ Scraping completed! Found {len(products)} products total.", file=sys.stderr)

    # Prepare output
    if args.output == "json":
        output = json.dumps(products, indent=2, ensure_ascii=False)
    else:  # csv
        if not products:
            output = ""
        else:
            output_io = io.StringIO()
            writer = csv.DictWriter(output_io, fieldnames=products[0].keys())
            writer.writeheader()
            writer.writerows(products)
            output = output_io.getvalue()

    # Write to file or stdout
    if args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Results saved to {args.file}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()