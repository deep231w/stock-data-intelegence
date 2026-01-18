from datetime import date, timedelta

def get_last_trading_day():
    today = date.today()
    weekday = today.weekday()  
    # Monday = 0, Sunday = 6

    if weekday == 0:      # Monday
        return today - timedelta(days=3)
    elif weekday == 6:    # Sunday
        return today - timedelta(days=2)
    elif weekday == 5:    # Saturday
        return today - timedelta(days=1)
    else:
        return today - timedelta(days=1)
