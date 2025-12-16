from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Music & Fashion Vibe App")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

from app.routers import web

app.include_router(web.router)

# Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/health")
def health_check():
    return {"status": "ok"}
