from fastapi import APIRouter ,HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.db  import get_db
from app.models.models import Company , StockPrice
from datetime import date,timedelta
from app.scripts.last_trading_day import get_last_trading_day
from app.scripts.download_data import fetch_stock_data
from app.core.insert_stock_data import insert_stock_data

router =APIRouter(prefix="/data", tags=["data"])

TICKERS = {
    "tcs": "TCS.NS",
    "hdfc": "HDFCBANK.NS",
    "mahindra": "M&M.NS",
    "google": "GOOGL",
}


@router.get("/{symbol}")
def get_data(symbol:str ,db:Session=Depends(get_db)):

    try:
        print("symbol is-", symbol)
        company = (
            db.query(Company)
            .filter(Company.symbol == symbol)
            .first()
        )

        if not company:
            raise HTTPException(status_code=400 , detail="company not found")
        print("company - ", company)

        stock_data= (
            db.query(StockPrice)
            .filter(StockPrice.company_id == company.id)
            .order_by(StockPrice.date.desc())
            .limit(30)
            .all()
        )
        
        last_trading_day= get_last_trading_day()

        print("latest db date:", stock_data[0].date if stock_data else None)
        print("last trading day:", last_trading_day)

        if not stock_data or stock_data[0].date != last_trading_day:
            print("refreshing stock data ....")
            df = fetch_stock_data(
                name=company.symbol,
                ticker=TICKERS[company.symbol]
            )
            insert_stock_data(db,company ,df)
            stock_data = (
                db.query(StockPrice)
                .filter(StockPrice.company_id == company.id)
                .order_by(StockPrice.date.desc())
                .limit(30)
                .all()
            )
        
        return {
            "company":company,
            "stock_data":stock_data
        }
    
    except ConnectionError as e:
        raise HTTPException(status_code=503 , detail="db connetion failed") from e
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"An unexpected error occurred: {e}") from e 
