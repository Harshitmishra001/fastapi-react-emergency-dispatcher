from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.security.auth import auth_router
from backend.db.models import init_db
from backend.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB. Shutdown: nothing extra needed for SQLite."""
    init_db()
    yield


app = FastAPI(title="Disaster Resource Coordinator API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
async def root_health():
    """Un-versioned health check for load balancers."""
    from datetime import datetime, timezone
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

# Auth router provides POST /token
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
# Main API router
app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

