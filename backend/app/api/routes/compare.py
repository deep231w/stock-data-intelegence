from fastapi import APIRouter

router = APIRouter(prefix="/compare",tags=["compare between 2 companies"])

@router.get("/")
def compare_bet_2_companies(symbol1:str, symbol2:str):
    
    return {symbol1 , symbol2}