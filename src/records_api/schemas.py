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

    @classmethod
    def calc_total(self) -> float:
        sum = 0
        for item in self.items:
            sum += item.amount
        return sum

class ExpenseType(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ACCOMODATION = "accommodation"
    OTHER = "other"
    NOT_APPLICABLE = "not_applicable"