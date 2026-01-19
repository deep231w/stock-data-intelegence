from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import StockPrice ,Company

router =APIRouter(prefix="/summary", tags=["Summary of company"])

@router.get("/{symbol}")
def fetch_summary(symbol:str,db:Session =Depends(get_db)):
    try:
        copmapy= (
            db.query(Company)
            .filter(Company.symbol==symbol)
            .first()
        )
        if not copmapy :
            raise HTTPException(status_code=400 , detail="company not found")
        
        latest_data= (
            db.query(
                StockPrice.ma_7,
                StockPrice.week52_high,
                StockPrice.week52_low
                )
            .filter(StockPrice.company_id == copmapy.id)
            .order_by(StockPrice.date.desc())
            .first()
        )
        if not latest_data:
            raise HTTPException(status_code=400, detail="latest data not found")

        return {
            "company": copmapy.symbol,
            "summary": {
                        "ma_7": latest_data.ma_7,
                        "week52_high": latest_data.week52_high,
                        "week52_low": latest_data.week52_low,
                    } if latest_data else None
            }
    except ConnectionError as e:
        raise HTTPException(status_code=503 , detail="db connetion failed") from e
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"An unexpected error occurred: {e}") from e 
