from fastapi import FastAPI
from schemas import Expense, LineItem, ExpenseType
from typing import Annotated

app = FastAPI()
