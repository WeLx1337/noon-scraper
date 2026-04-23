from curl_cffi import requests as cf_requests
from bs4 import BeautifulSoup
import re, time
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def clean_price(raw):
    if not raw:
        return None
    # Find all price-like sequences (numbers with commas)
    prices = re.findall(r"\d{1,3}(?:,\d{3})*", raw)
    if not prices:
        return None
    
    # Filter out small numbers (like discount percentages < 100)
    valid_prices = [p for p in prices if int(p.replace(",", "")) >= 100]
    if not valid_prices:
        # If no valid prices, take the last one
        clean_str = prices[-1].replace(",", "")
    else:
        # Take the minimum of valid prices (assuming discounted is lower)
        clean_str = min(valid_prices, key=lambda x: int(x.replace(",", ""))).replace(",", "")
    
    try:
        return int(clean_str)
    except ValueError:
        return None

def scrape_noon(query, pages=2, country="saudi", progress_callback=None):
    all_products = [] 
    
    domain_map = {
        "saudi": "saudi-en",
        "uae": "uae-en",
        "egypt": "egypt-en"
    }
    
    domain_path = domain_map.get(country, "saudi-en") 

    for page in range(1, pages + 1):
        if progress_callback:
            progress_callback(f"Starting page {page}/{pages}...")
        
        url = f"https://www.noon.com/{domain_path}/search/?q={query}&page={page}"
        try:
            r = cf_requests.get(url, headers=HEADERS, impersonate="chrome", timeout=20)
            if r.status_code != 200:
                if progress_callback:
                    progress_callback(f"Page {page} returned status {r.status_code}, stopping...")
                break
            
            soup = BeautifulSoup(r.text, "html.parser")
            cards = soup.find_all(attrs={"data-qa": "plp-product-box"})
            
            if not cards:
                if progress_callback:
                    progress_callback(f"No products found on page {page}, stopping...")
                break
                
            page_products = 0
            for card in cards:
                name_el  = card.find(attrs={"data-qa": "plp-product-box-name"})
                price_el = card.find(attrs={"data-qa": "plp-product-box-price"})
                link_el  = card.find("a", href=True)
                img_el   = card.find("img")
                badge_el = card.find(attrs={"data-qa": "product-noon-express"})

                name = name_el.get_text(strip=True) if name_el else "N/A"

                # Try to find the specific 'amount' span first, then fallback to full text
                if price_el:
                    amount_els = price_el.find_all(class_="amount")
                    if amount_els:
                        raw_price_text = amount_els[-1].get_text(strip=True)  # Take the last amount (discounted price)
                    else:
                        raw_price_text = price_el.get_text(strip=True)
                else:
                    raw_price_text = ""
                
                price = clean_price(raw_price_text)
                link  = "https://www.noon.com" + link_el["href"] if link_el else "#"
                # Find the real product image (not the placeholder)
                img_el = card.find("img", class_=lambda c: c and "productImage" in c)
                if not img_el:
                    # Fallback: find img with src containing product path
                    img_el = card.find("img", src=lambda s: s and "/p/pnsku/" in s)
                img = img_el.get("src", "") if img_el else ""
                express = bool(badge_el)

                if name != "N/A":
                    all_products.append({
                        "name": name,
                        "price": price if price is not None else 0,
                        "link": link,
                        "img": img,
                        "express": express,
                    })
                    page_products += 1
                    page_products += 1
            
            if progress_callback:
                progress_callback(f"Page {page}/{pages} completed: found {page_products} products (total: {len(all_products)})")
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error on page {page}: {e}")
            break
        
        # Friendly reminder to stay below the radar
        time.sleep(1.2)
        
    if progress_callback:
        progress_callback(f"Scraping completed: {len(all_products)} total products found")
        
    return all_products