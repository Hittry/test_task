#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import argparse
import aiohttp
import asyncio

URL = 'http://0.0.0.0:8080/task'


async def ticker(number_task: int):
    for count in range(number_task):
        yield count


async def main():
    params_post = {'attachment_depth': args.depth}
    async with aiohttp.ClientSession() as session:
        async for count in ticker(args.number):
            async with session.post(URL, params=params_post) as post_resp:
                answer = await post_resp.json()
                req_uuid = answer['request_uuid']
                params_get = {'request_uuid': req_uuid}
            async with session.get(URL, params=params_get) as get_resp:
                compare_id_uuid = await get_resp.text()
                print(f"Выполнено: {count}, всего: {args.number}")


# определяем аргументы коммандной строки
aparser = argparse.ArgumentParser(description='Скрипт сохранения req данных в БД и выгрузки id из нее')
aparser.add_argument('-d', '--depth', required=True, type=int, help="Глубина вложенности json файла")
aparser.add_argument('-N', '--number', required=True, type=int, help="Чило запросов")

if __name__ == '__main__':
    args = aparser.parse_args()
    asyncio.run(main())
