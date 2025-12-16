class VibeTranslator:
    def __init__(self):
        self.mapping = {
            "Grunge": {
                "vibe": "90s Underground",
                "keywords": ["Flannel shirt", "Ripped jeans", "Combat boots", "Oversized cardigan", "Beanies"]
            },
            "Rock": {
                "vibe": "Classic Rocker",
                "keywords": ["Leather jacket", "Band t-shirt", "Denim jacket", "Chelsea boots", "Aviator sunglasses"]
            },
            "Synth-pop": {
                "vibe": "Retro Future",
                "keywords": ["Neon windbreaker", "Metallic sneakers", "Bomber jacket", "Retro sunglasses", "Shiny leggings"]
            },
            "Pop": {
                "vibe": "Mainstream Chic",
                "keywords": ["Trendy crop top", "High-waisted jeans", "White sneakers", "Statement earrings", "Mini bag"]
            },
            "Disco": {
                "vibe": "Studio 54",
                "keywords": ["Sequin dress", "Platform shoes", "Velvet blazer", "Flared trousers", "Glitter accessories"]
            }
        }
        self.default_vibe = {
            "vibe": "Casual Daily",
            "keywords": ["T-shirt", "Jeans", "Sneakers", "Hoodie", "Baseball cap"]
        }

    def get_vibe(self, genres):
        for genre in genres:
            if genre in self.mapping:
                return self.mapping[genre]
        return self.default_vibe
