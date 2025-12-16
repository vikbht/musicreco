from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.apple_music import AppleMusicClient
from app.services.vibes import VibeTranslator
from app.services.amazon import AmazonClient

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

music_client = AppleMusicClient()
vibe_translator = VibeTranslator()
amazon_client = AmazonClient()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    # 1. Search Song/Artist
    song_data = music_client.search_song(query)
    
    if not song_data:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": "No music found.",
            "query": query
        })

    # 2. Determine Vibe
    vibe_data = vibe_translator.get_vibe(song_data.get("genres", []))
    
    # 3. Get Recommendations
    products = amazon_client.search_products(vibe_data["keywords"])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "song": song_data,
        "vibe": vibe_data,
        "products": products,
        "query": query
    })
