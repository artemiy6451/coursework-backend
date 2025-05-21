from collections import Counter, defaultdict
from datetime import date, datetime

from app.user.schemas import HeatmapField, TimeData


def get_total_time(time_data: list[TimeData]) -> int:
    total_spent_time = sum(td.delta for td in time_data)
    return total_spent_time


def get_average_time_per_day(time_data: list[TimeData]) -> int:
    time_by_day: dict[date, int] = defaultdict(int)

    for td in time_data:
        day = td.session_start.date()
        time_by_day[day] += td.delta

    total_days = len(time_by_day)
    total_minutes = sum(time_by_day.values())

    average = total_minutes // total_days if total_days else 0
    return average


def get_average_time_per_week(time_data: list[TimeData]) -> int:
    time_by_week: dict[tuple[int, int], int] = defaultdict(int)

    for td in time_data:
        year, week, _ = td.session_start.isocalendar()
        key = (year, week)
        time_by_week[key] += td.delta

    total_weeks = len(time_by_week)
    total_minutes = sum(time_by_week.values())

    average = total_minutes // total_weeks if total_weeks else 0
    return average


def get_average_time_per_month(time_data: list[TimeData]) -> int:
    time_by_month: dict[tuple[int, int], int] = defaultdict(int)

    for td in time_data:
        year = td.session_start.year
        month = td.session_start.month
        key = (year, month)
        time_by_month[key] += td.delta

    total_months = len(time_by_month)
    total_minutes = sum(time_by_month.values())

    average = total_minutes // total_months if total_months else 0
    return average


def get_most_visited_day_of_month(time_data: list[TimeData]) -> str:
    day_counts = Counter(td.session_start.strftime("%A").lower() for td in time_data)

    most_common_day, _ = day_counts.most_common(1)[0]

    return most_common_day


def get_most_visited_time_of_month(time_data: list[TimeData]) -> str:
    time_counts = Counter(
        td.session_start.replace(minute=0, second=0, microsecond=0).strftime("%H:%M")
        for td in time_data
    )

    most_common_time, _ = time_counts.most_common(1)[0]
    return most_common_time


def get_heatmap(time_data: list[TimeData]) -> list[HeatmapField]:
    heatmap: dict[date, int] = defaultdict(int)

    for td in time_data:
        day = td.session_start.date()
        heatmap[day] += td.delta

    result = [
        HeatmapField(date=datetime.combine(day, datetime.min.time()), count=minutes)
        for day, minutes in sorted(heatmap.items())
    ]

    return result
