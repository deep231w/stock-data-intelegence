from fastapi import APIRouter ,Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Company
router= APIRouter(prefix="/companies" , tags=["companies"])

@router.get("/")
def get_companies (db:Session =Depends(get_db)):
    companies = db.query(Company).all()
    print("companies in fetch companies router- ", companies)
    
    return companies
