from fastapi import FastAPI,Depends
from schemas import Expense, LineItem, ExpenseType
from typing import Annotated
from auth.utils import validate_token

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/protected",dependencies=[Depends(validate_token)])
def protected():
    return {"message": "valid token"}