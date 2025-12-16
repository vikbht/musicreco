import os
import random
from amazon_paapi import AmazonApi
from dotenv import load_dotenv

load_dotenv()

class AmazonClient:
    def __init__(self):
        self.access_key = os.getenv("AMAZON_ACCESS_KEY")
        self.secret_key = os.getenv("AMAZON_SECRET_KEY")
        self.partner_tag = os.getenv("AMAZON_PARTNER_TAG")
        
        self.amazon = None
        if self.access_key and self.secret_key and self.partner_tag:
            try:
                self.amazon = AmazonApi(self.access_key, self.secret_key, self.partner_tag, "US")
            except Exception as e:
                print(f"Failed to initialize Amazon API: {e}")

    def search_products(self, keywords):
        if self.amazon:
            try:
                return self._real_search(keywords)
            except Exception as e:
                print(f"Amazon API Search failed: {e}. Falling back to mock.")
                # Fallback to mock if API fails (e.g., throttling, invalid keys)
                return self._mock_search(keywords)
        else:
            return self._mock_search(keywords)

    def _real_search(self, keywords):
        # Construct a search query from keywords
        search_query = " ".join(keywords[:2]) # Use first 2 keywords for broader match
        
        products = []
        try:
            items = self.amazon.search_items(keywords=search_query, item_count=4)
            for item in items.items:
                # Extract high-res image if available
                image_url = item.images.primary.large.url if item.images.primary else "https://placehold.co/300x400?text=No+Image"
                
                products.append({
                    "title": item.item_info.title.display_value,
                    "price": item.offers.listings[0].price.display_amount if item.offers and item.offers.listings else "N/A",
                    "image_url": image_url,
                    "link": item.detail_page_url
                })
        except Exception as e:
            print(f"Error fetching items: {e}")
            raise e # Re-raise to trigger fallback

        return products

    def _mock_search(self, keywords):
        # Return dummy products with nice placeholders
        products = []
        # Themes for loremflickr to ensure variety
        modifiers = ["fashion", "style", "clothing", "outfit"]
        
        for i, keyword in enumerate(keywords[:4]): 
            # Use random seed based on keyword to keep it deterministic-ish per keyword
            random_seed = random.randint(1, 1000)
            
            # Construct a LoremFlickr URL
            # format: https://loremflickr.com/{width}/{height}/{keywords}
            image_url = f"https://loremflickr.com/300/400/{keyword.replace(' ', ',')},fashion?random={i}"
            
            products.append({
                "title": f"Premium {keyword} (Style Edit)",
                "price": f"${(i+1) * 25}.99",
                "image_url": image_url,
                "link": f"https://amazon.com/s?k={keyword.replace(' ', '+')}"
            })
        return products
