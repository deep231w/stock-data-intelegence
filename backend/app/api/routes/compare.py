from fastapi import APIRouter, Depends, HTTPException
from app.models.models import Company, StockPrice
from sqlalchemy.orm import Session
from app.core.db import get_db
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

        return {symbol1 , symbol2}
    except ConnectionError as e:
        raise HTTPException(status_code=500 , detail="db connetion failed") from e
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"an unexpected error: {e}") from e