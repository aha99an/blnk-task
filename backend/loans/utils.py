from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_loan_settlement_amount(
    loan_amount: float, loan_duration: int, loan_rate: float
):
    """
    Get the settlement amount for a certian loan/fund
    """
    total_rate = loan_rate * loan_duration
    interest = (loan_amount * total_rate) / 100
    return loan_amount + interest


def get_same_day_from_next_months(months_number: int, start_date: datetime) -> list:
    """
    get the same day date for the next {months_number} starting the next month of {start_date}
    """
    dates = []
    for _ in range(months_number):
        date_after_month = start_date + relativedelta(months=1)
        dates.append(str(date_after_month.strftime("%d-%B-%Y")))
        start_date = date_after_month
    return dates
