from datetime import datetime, timedelta
from random import randint
from typing import Generator

from conf import *


def datetime_to_timestamp(dt: datetime) -> int:
    return round(dt.timestamp() * 1000, 0)


def get_datetime_in_iso_format(_datetime: datetime, _format: bool = True) -> str:
    if not _format:
        return _datetime

    return _datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def get_random_value(min_value: int, max_value: int) -> int:
    return randint(min_value, max_value)


def timestamp_difference(timestamp1: int, timestamp2: int) -> int:
    if timestamp1 > timestamp2:
        raise ValueError("Timestamp 1 should be less than Timestamp 2")

    return abs(timestamp1 - timestamp2)


def get_random_datetime_between_two_dates(
    start_date: datetime, end_date: datetime
) -> Generator[str, int, None]:
    summ_of_increment = 0
    cp_datetime = start_date
    difference_in_secs = (end_date - start_date).total_seconds()

    while summ_of_increment < difference_in_secs:
        increment = get_random_value(1, 20)
        summ_of_increment += increment

        cp_datetime += timedelta(seconds=increment)
        yield (
            get_datetime_in_iso_format(_datetime=cp_datetime),
            datetime_to_timestamp(dt=cp_datetime),
        )


def sec_to_millisec(sec: int) -> int:
    return sec * 1000


def get_timzone_substracted(dt: datetime) -> datetime:
    return dt - timedelta(hours=5, minutes=30)


def get_row_dict(
    id: int,
    timestamp_start: str,
    timestamp: str,
    duration: int,
) -> dict:
    randint = get_random_value(0, len(APP_SOURCE) - 1)
    app_source = APP_SOURCE[randint]
    return {
        "id": id,
        "type": "PLUGIN",
        "userId": USER_ID,
        "appTitle": app_source[0],
        "appName": app_source[1],
        "appPath": app_source[2],
        "description": app_source[3],
        "matterId": None,
        "appId": 0,
        "source": SOURCE,
        "userRate": USER_RATE,
        "updatedByUserId": UPDATED_BY_ID,
        "matterTaskId": MATTER_TASK_ID,
        "matterSubTaskId": MATTER_SUB_TASK_ID,
        "subTypeId": SUBTYPE_ID,
        "timestampStart": timestamp_start,
        "Timestamp": timestamp,
        "duration": duration,
    }


def get_columns_and_placeholders(
    start_id: int, start_date: datetime, end_date: datetime
) -> Generator[tuple, list, None]:
    for i, (timestamp_start, timestamp) in enumerate(
        get_random_datetime_between_two_dates(start_date, end_date)
    ):
        duration = get_random_value(1, 20)
        row_dict = get_row_dict(
            id=start_id + i,
            timestamp_start=timestamp_start,
            timestamp=timestamp,
            duration=sec_to_millisec(duration),
        )
        yield list(row_dict.keys()), list(row_dict.values())
