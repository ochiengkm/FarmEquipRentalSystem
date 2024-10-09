# utils.py

from datetime import date, timedelta


def book_fine_calculation(borrowing_date, return_date):
    due_date = borrowing_date + timedelta(days=14)  # Assuming a 14-day borrowing period
    if return_date > due_date:
        days_overdue = (return_date - due_date).days
        fine_amount = days_overdue * 0.50  # Adjust the fine amount as needed
        return fine_amount
    else:
        return 0
