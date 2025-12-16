import os
import requests

class AppleMusicClient:
    def __init__(self):
        self.developer_token = os.getenv("APPLE_MUSIC_TOKEN")
        self.is_mock = not self.developer_token

    def search_song(self, query):
        if self.is_mock:
            return self._mock_search(query)
        
        # TODO: Implement real API call
        pass

    def _mock_search(self, query):
        # Return a deterministic mock result based on query
        query_lower = query.lower()
        if "nirvana" in query_lower:
            return {
                "id": "mock_1",
                "name": "Smells Like Teen Spirit",
                "artist": "Nirvana",
                "album": "Nevermind",
                "artwork": "https://upload.wikimedia.org/wikipedia/en/b/b7/NirvanaNevermindalbumcover.jpg",
                "genres": ["Grunge", "Rock"]
            }
        elif "weekend" in query_lower:
             return {
                "id": "mock_2",
                "name": "Blinding Lights",
                "artist": "The Weeknd",
                "album": "After Hours",
                "artwork": "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Weeknd_-_After_Hours.png",
                "genres": ["Synth-pop", "R&B"]
            }
        else:
             return {
                "id": "mock_3",
                "name": "Levitating",
                "artist": "Dua Lipa",
                "album": "Future Nostalgia",
                "artwork": "https://upload.wikimedia.org/wikipedia/en/f/f5/Dua_Lipa_-_Future_Nostalgia_%28Official_Album_Cover%29.png",
                "genres": ["Pop", "Disco"]
            }

    def get_song_details(self, song_id):
        # In a real app, we might need a separate call. 
        # For mock, we can just return a generic structure or reuse search.
        pass
