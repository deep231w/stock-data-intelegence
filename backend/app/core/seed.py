from app.core.db import SessionLocal
from app.models.models import Company

TICKERS ={
    "tcs",
    "hdfc",
    "mahindra",
    "google"
}

def seed_companies():

    db=SessionLocal()
    try:
        for symbol in TICKERS:
            existing =db.query(Company).filter(Company.symbol == symbol).first()
            if not existing:
                company= Company(symbol=symbol)
                db.add(company)

        db.commit()
        print("companies added successfully")

    finally:
        db.close()

if __name__ == "__main__":
    seed_companies()