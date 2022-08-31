from datetime import datetime


def year_validator(year):
    now = datetime.now()
    year_now = now.year
    if year > year_now:
        raise ValueError(f'Указанный год больше текущего {year}')
