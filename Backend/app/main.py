from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.api.v1.web_api.router import web_api_router

app = FastAPI(title=settings.APP_NAME)

if settings.CORS_ORIGINS == "*":
    origins = ["*"]
else:
    origins = [
        origin.strip()
        for origin in settings.CORS_ORIGINS.split(",")
        if origin.strip()
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(web_api_router, prefix=f"{settings.API_V1_PREFIX}/web_api")

# Optional single-service web hosting mode.
# Local Docker Compose keeps React in its own Vite container. When WEB_DIST_DIR
# points to a built React `dist` directory, FastAPI also serves that dashboard so
# a public demo can use one URL for both the UI and API.
import os
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

_web_dist_value = os.getenv("WEB_DIST_DIR", "").strip()
if _web_dist_value:
    _web_dist = Path(_web_dist_value).resolve()
    _index_file = _web_dist / "index.html"

    if _index_file.is_file():
        _assets_dir = _web_dist / "assets"
        if _assets_dir.is_dir():
            app.mount("/assets", StaticFiles(directory=str(_assets_dir)), name="web-assets")

        @app.get("/", include_in_schema=False)
        def serve_dashboard_root():
            return FileResponse(_index_file)

        @app.get("/{full_path:path}", include_in_schema=False)
        def serve_dashboard_spa(full_path: str):
            candidate = (_web_dist / full_path).resolve()
            # Serve generated root-level files such as favicon assets, but never
            # allow a path to escape the configured web build directory.
            if candidate.is_file() and (candidate == _web_dist or _web_dist in candidate.parents):
                return FileResponse(candidate)
            return FileResponse(_index_file)

