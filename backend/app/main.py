from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import bookings, courts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rally Courts API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courts.router)
app.include_router(bookings.router)


@app.get("/")
def root():
    return {"message": "Rally Courts API"}
