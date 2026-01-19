from fastapi import FastAPI;
from app.api.routes import companies, data,summary ,compare
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
app.include_router(data.router)
app.include_router(summary.router)
app.include_router(compare.router)