from fastapi import FastAPI;
from app.api.routes import companies
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "fastapi Server running "}

app.include_router(companies.router)