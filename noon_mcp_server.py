from mcp.server.fastmcp import FastMCP
from scraper import scrape_noon  # Import your existing logic

# Initialize FastMCP
mcp = FastMCP("Noon Search Tool")

@mcp.tool()
def search_noon_products(query: str, country: str = "saudi", pages: int = 1) -> str:
    """
    Searches Noon.com for products and returns a list of results.
    
    Args:
        query: The product to search for (e.g., 'iPhone 15').
        country: The market to search in ('saudi', 'uae', or 'egypt').[cite: 1]
        pages: Number of pages to crawl (default 1 for speed).[cite: 1]
    """
    try:
        # Use your existing scrape_noon function
        products = scrape_noon(query, pages=pages, country=country)
        
        if not products:
            return f"No products found for '{query}' in {country}."

        # Format results for the LLM to read easily
        formatted_results = []
        for p in products:
            status = "[Express]" if p['express'] else ""
            formatted_results.append(
                f"- {p['name']}\n  Price: {p['price']} SAR/AED/EGP {status}\n  Link: {p['link']}"
            )
            
        return "\n\n".join(formatted_results)
    
    except Exception as e:
        return f"An error occurred during the search: {str(e)}"

if __name__ == "__main__":
    mcp.run()