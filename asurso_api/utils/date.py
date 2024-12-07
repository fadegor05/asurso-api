from datetime import datetime, timedelta, date


def get_week_interval_by_date(current_date: date) -> (datetime, datetime):
    current_datetime = datetime.combine(current_date, datetime.min.time())
    start_datetime = current_datetime - timedelta(days=current_datetime.isoweekday() - 1)
    end_datetime = start_datetime + timedelta(days=6)
    return start_datetime, end_datetime
