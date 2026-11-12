from pydantic import BaseModel
from enum import Enum

class LineItem(BaseModel):
    description:str
    amount:float

class Expense(BaseModel):
    shop_name:str
    items:list[LineItem]
    category:ExpenseType
    total:float

class ExpenseType(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ACCOMODATION = "accommodation"
    OTHER = "other"
    NOT_APPLICABLE = "not_applicable"
