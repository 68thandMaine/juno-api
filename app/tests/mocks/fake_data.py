from uuid import uuid4

bill_for_tests = {
    "id": str(uuid4()),
    "name": "TEST_BILL",
    "amount": 12,
    "due_date": "11/12/2025",
    "category": None,
    "paid": 1,
    "recurring": False,
    "recurrence_interval": None,
    "auto_pay": False,
}

payment_for_tests = {
    "amount": 12.22,
    "payment_date": "11/12/2025",
    "bill_id": None,
}
