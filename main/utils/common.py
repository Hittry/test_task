import datetime

# Поля БД
ID = 'id'
REQUEST_UUID = 'request_uuid'
REQUEST_DATE = 'request_date'
ATTACHMENT = 'attachment'

# Подключение к БД
DEFAULT_PORT = '5432'
USER = 'user'
PASSWORD = 'password'
HOST = 'localhost'
ATTACHMENT_DEPTH = 'attachment_depth'

ENTITY = 'entity'

DATE_FORMAT = '%d/%m/%y %H:%M:%S'


async def tick_reversed_numbers(depth: int):
    for count in reversed(range(depth - 1)):
        yield count


async def correct_form(dt: str) -> datetime:
    date_time = datetime.datetime.strptime(dt, DATE_FORMAT) if dt else datetime.datetime.utcnow()
    return date_time


async def build_json_by_depth(depth: int) -> dict:
    result = [{ENTITY: {}}]
    async for _ in tick_reversed_numbers(depth):
        dict_for_level = {ENTITY: result[0]}
        del result[0]
        result.append(dict_for_level)
    return result[0]
