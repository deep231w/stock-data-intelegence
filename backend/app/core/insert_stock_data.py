from sqlalchemy.orm import Session
from app.models.models import Company, StockPrice

def insert_stock_data(
    db: Session,
    company: Company,
    df
):
    for _, row in df.iterrows():
        exists = (
            db.query(StockPrice)
            .filter(
                StockPrice.company_id == company.id,
                StockPrice.date == row["date"].date()
            )
            .first()
        )

        if exists:
            continue  # skip duplicates

        stock = StockPrice(
            company_id=company.id,
            date=row["date"].date(),
            open=row["open"],
            close=row["close"],
            high=row["high"],
            low=row["low"],
            daily_return=row["daily_return"],
            ma_7=row["ma_7"],
            week52_high=row["week52_high"],
            week52_low=row["week52_low"],
        )

        db.add(stock)

    db.commit()
