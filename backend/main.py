import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.db.models import init_db

app = FastAPI(title="Disaster Resource Coordinator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In prod, lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
