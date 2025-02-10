import re
from datetime import timedelta
from typing import Union


def parse_duration(duration: str) -> Union[timedelta, None]:
    if isinstance(duration, str):
        pattern = r'(?P<value>\d+(\.\d+)?)(?P<unit>[hms])'
        match = re.match(pattern, duration)
        if not match:
            return None

        value = float(match.group('value'))
        unit = match.group('unit')

        match unit:
            case 'h':
                return timedelta(hours=value)
            case 'm':
                return timedelta(minutes=value)
            case 's':
                return timedelta(seconds=value)
    return None


async def is_user_muted(chat_id: int, user_id: int) -> bool:
    if isinstance(chat_id, int) and isinstance(user_id, int):
        ...
    raise ValueError('User ID or Chat ID is not a int')
