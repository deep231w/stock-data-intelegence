from sqlalchemy import Column ,Integer , String, Float ,Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base =declarative_base()

class Company(Base):
    __tablename__="companies"

    id =Column(Integer,primary_key=True)
    symbol=Column(String, unique=True , index=True)

    prices= relationship("StockPrice", back_populates="company")

class StockPrice(Base):
    __tablename__="stock_prices"

    id=Column(Integer , primary_key=True )
    company_id= Column(Integer, ForeignKey("companies.id"), index=True)
    date= Column(Date, index=True)

    open=Column(Float)
    close=Column(Float)
    high=Column(Float)
    low=Column(Float)
    
    daily_return=Column(Float)

    ma_7=Column(Float)
    week52_high=Column(Float)
    week52_low=Column(Float)

    company =relationship("Company", back_populates="prices")