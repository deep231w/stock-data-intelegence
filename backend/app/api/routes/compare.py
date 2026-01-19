from fastapi import APIRouter, Depends, HTTPException
from app.models.models import Company, StockPrice
from sqlalchemy.orm import Session
from app.core.db import get_db
from sqlalchemy import func
import math

router = APIRouter(prefix="/compare",tags=["compare between 2 companies"])

def calculate_metrics(prices):
    """
    prices: list of StockPrice (latest 30 days, DESC order)
    """
    prices = list(reversed(prices))  # oldest → latest

    first_close = prices[0].close
    last_close = prices[-1].close

    return_percent = ((last_close - first_close) / first_close) * 100

    daily_returns = [p.daily_return for p in prices if p.daily_return is not None]

    mean = sum(daily_returns) / len(daily_returns)
    variance = sum((x - mean) ** 2 for x in daily_returns) / len(daily_returns)
    volatility = math.sqrt(variance)

    return round(return_percent, 2), round(volatility, 4)


@router.get("/")
def compare_bet_2_companies(symbol1:str, symbol2:str, db:Session=Depends(get_db)):
    try:
        company1 =(
            db.query(Company)
            .filter(Company.symbol == symbol1)
            .first()
        )
        company2=(
            db.query(Company)
            .filter(Company.symbol ==symbol2)
            .first()
        )
        if not company1 or not company2:
            raise HTTPException(status_code=404, detail="Company not found")
        
        prices1 = (
            db.query(StockPrice)
            .filter(StockPrice.company_id == company1.id)
            .order_by(StockPrice.date.desc())
            .limit(30)
            .all()
        )

        prices2 = (
            db.query(StockPrice)
            .filter(StockPrice.company_id == company2.id)
            .order_by(StockPrice.date.desc())
            .limit(30)
            .all()
        )

        if len(prices1) < 2 or len(prices2) < 2:
            raise HTTPException(status_code=400, detail="Not enough data")

        ret1, vol1 = calculate_metrics(prices1)
        ret2, vol2 = calculate_metrics(prices2)


        return {
            "period": "last_30_days",
            "stock_1": {
                "symbol": symbol1,
                "return_percent": ret1,
                "volatility": vol1
            },
            "stock_2": {
                "symbol": symbol2,
                "return_percent": ret2,
                "volatility": vol2
            },
            "comparison": {
                "better_return": symbol1 if ret1 > ret2 else symbol2,
                "more_volatile": symbol1 if vol1 > vol2 else symbol2
            }
        }
    except ConnectionError as e:
        raise HTTPException(status_code=500 , detail="db connetion failed") from e
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"an unexpected error: {e}") from e