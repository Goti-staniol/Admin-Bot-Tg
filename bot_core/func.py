from textwrap import dedent
from datetime import timedelta
from typing import Union

import yaml
import re


def load_texts() -> dict:
    with open('bot_core/data/texts.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def remove_dedent(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError('String Expected')
    return dedent(text)

def parse_duration(duration: str) -> Union[timedelta, None]:
    if not isinstance(duration, str):
        raise ValueError('String Expected')

    pattern = r'(?P<value>\d+(\.\d+)?)(?P<unit>[hmsdw])'
    match = re.match(pattern, duration)
    if not match:
        raise ValueError(
            "Invalid format. Expected examples: '10h', '15.5m', or '30s'."
        )

    value = float(match.group('value'))
    unit = match.group('unit')
    match unit:
        case 'h':
            return timedelta(hours=value)
        case 'm':
            return timedelta(minutes=value)
        case 's':
            return timedelta(seconds=value)
        case 'd':
            return timedelta(days=value)
        case 'w':
            return timedelta(weeks=value)
        case _:
            raise ValueError(f"Unknown time unit: {unit}. Expected 'h', 'm', 'd', or 's'.")

async def is_user_muted(chat_id: int, user_id: int) -> bool:
    if not (isinstance(chat_id, int) and isinstance(user_id, int)):
        raise ValueError('User ID or Chat ID is not a int')
