from fastapi import FastAPI, Request
from schemas import Expense, LineItem, ExpenseType
from routes.records import router as records_router
import time

app = FastAPI(routes=records_router)


