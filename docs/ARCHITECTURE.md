# SonicStyle Software Architecture

## Overview
**SonicStyle** is a web application that bridges the gap between music and fashion. It analyzes the "vibe" of a user's music choice (artist, song, album) and recommends fashion items that match that aesthetic.

## System Context (C4 Level 1)
The following diagram illustrates the high-level context of the SonicStyle system and its external dependencies.

```mermaid
C4Context
    title System Context Diagram for SonicStyle

    Person(user, "User", "A music and fashion enthusiast.")
    System(sonic_style, "SonicStyle Web App", "Allows users to search for music and see matching fashion recommendations.")

    System_Ext(apple_music, "Apple Music API", "Provides song details, genres, and artist information.")
    System_Ext(amazon, "Amazon Product API", "Provides fashion product search results and affiliate links.")

    Rel(user, sonic_style, "Searches for music, Views products", "HTTPS")
    Rel(sonic_style, apple_music, "Fetches song metadata & genres", "HTTPS/JSON")
    Rel(sonic_style, amazon, "Searches for products by keywords", "HTTPS/JSON")
```

## Container Diagram (C4 Level 2)
This diagram shows the high-level breakdown of the internal containers and components.

```mermaid
C4Container
    title Container Diagram for SonicStyle

    Person(user, "User", "Using a web browser")

    Container_Boundary(c1, "SonicStyle Application") {
        Container(web_frontend, "Web Frontend", "HTML, CSS, JS (Jinja2)", "Delivers the user interface via server-side rendering.")
        Container(fastapi_app, "Backend API", "Python, FastAPI", "Handles request routing, orchestration, and business logic.")
    }

    System_Ext(apple_music, "Apple Music API", "Provides song details, genres, and artist information.")
    System_Ext(amazon, "Amazon Product API", "Provides fashion product search results and affiliate links.")

    Rel(user, web_frontend, "Visits", "HTTPS")
    Rel(web_frontend, fastapi_app, "Submits Forms/Requests", "HTTPS")
    
    Rel(fastapi_app, apple_music, "Fetches song data", "HTTPS")
    Rel(fastapi_app, amazon, "Searches products", "HTTPS")
```

## Sequence Diagram: Search Flow
The core workflow of the application is the search process.

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web Router
    participant M as Apple Music Client
    participant V as Vibe Service
    participant A as Amazon Client
    participant T as Templates

    U->>W: POST /search (query="Nirvana")
    
    W->>M: search_song("Nirvana")
    alt Music Found
        M-->>W: Song Data (Genre: "Grunge")
    else No Music Found
        M-->>W: None
        W->>U: Render Error Page
    end

    W->>V: get_vibe(["Grunge"])
    V-->>W: Vibe Data (Style: "90s Underground", Keywords: ["Flannel", "Boots"])

    W->>A: search_products(["Flannel", "Boots"])
    A-->>W: Product List (Title, Price, Image, Link)

    W->>T: TemplateResponse("index.html", data)
    T-->>U: Render HTML Page
```

## Project Structure
The code is organized as a modular FastAPI application managed by `uv`.

```
musicreco/
├── app/
│   ├── main.py              # Application Entry Point
│   ├── routers/
│   │   └── web.py           # Web Routes (Search Logic)
│   ├── services/
│   │   ├── apple_music.py   # Music API Wrapper
│   │   ├── amazon.py        # Shopping API Wrapper
│   │   └── vibes.py         # Business Logic (Vibe Translation)
│   ├── static/
│   │   └── css/
│   │       └── style.css    # Premium Styling
│   └── templates/
│       └── index.html       # Main UI Template
├── pyproject.toml           # Dependency Management (uv)
└── uv.lock                  # Locked Dependencies
```

## Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Language** | Python 3.12+ | Rich ecosystem, ease of API integration. |
| **Framework** | FastAPI | High performance, async support, easy to structure. |
| **Dependency Manager** | uv | Extremely fast, reliable modern package management. |
| **Templating** | Jinja2 | Standard for Python server-side rendering. |
| **Styling** | Vanilla CSS3 | Custom high-end "Glassmorphism" design without framework bloat. |
| **Server** | Uvicorn | ASGI server for production-grade performance. |

## Design Decisions
1.  **Mock Mode Logic**: To reduce friction for new developers (and evaluation), the API Clients (`AppleMusicClient`, `AmazonClient`) are designed to seamlessly switch to "Mock Mode" if API keys are not detected in the environment. This ensures the app is always runnable.
2.  **Server-Side Rendering (SSR)**: Chosen over a SPA (Single Page App) for simplicity and speed of development given the purely informational/search-based nature of the initial requirements.
3.  **Vibe Dictionary**: The mapping logic is currently purely rule-based (Genre -> Keywords) mapped in `vibes.py`. This allows for deterministic testing before implementing more complex AI/ML matching logic.
