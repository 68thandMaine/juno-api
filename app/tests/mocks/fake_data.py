import datetime
from uuid import uuid4

bill_for_tests = {
    "id": str(uuid4()),
    "name": "TEST_BILL",
    "amount": 12,
    "due_date": datetime.date.today().strftime("%Y-%m-%d"),  # < this is a string
    "category": None,
    "paid": 1,
    "recurring": False,
    "recurrence_interval": None,
    "auto_pay": False,
}

payment_for_tests = {
    "amount": 12.22,
    "payment_date": datetime.date.today().strftime("%Y-%m-%d"),
    "bill_id": None,
}
