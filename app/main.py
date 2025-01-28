from fastapi import FastAPI
from app.api import reviews
from app.database import engine, Base

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/docs")

# Include API routers
app.include_router(reviews.router)


@app.get("/status")
def read_root():
    return {"status": "ok"}
