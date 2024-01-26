import datetime

bill_for_tests = {
    "name": "TEST_BILL",
    "amount": 12,
    "due_date": datetime.date.today().strftime("%Y-%m-%d"),
    "category": None,
    "status": 1,
    "recurring": False,
    "recurrence_interval": "MONTHLY",
}

payment_for_tests = {
    "amount": 12.22,
    "payment_date": datetime.date.today().strftime("%Y-%m-%d"),
    "bill_id": None,
}
