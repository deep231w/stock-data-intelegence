from fastapi import FastAPI;
from app.api.routes import companies
app= FastAPI()

@app.get("/")
def root():
    return {"message": "fastapi Server running "}

app.include_router(companies.router)