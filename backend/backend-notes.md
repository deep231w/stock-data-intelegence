## FastAPI DB pattern

def endpoint(db: Session = Depends(get_db)):
    db.query(Model).filter(...).all()
