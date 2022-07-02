import uuid

import common as ut_common
from schema import Base, TableSchema

import aiohttp_sqlalchemy as ah_sa
from aiohttp_swagger import setup_swagger
from aiohttp import web
from sqlalchemy import select

routes = web.RouteTableDef()

DEFAULT_PORT = '5432'

USER = 'user'
PASSWORD = 'password'
HOST = 'db'


async def app_start():
    app = web.Application()
    ah_sa.setup(app, [
        ah_sa.bind(f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{DEFAULT_PORT}/postgres'),
    ])
    await ah_sa.init_db(app, Base.metadata)
    app.add_routes(routes)
    setup_swagger(app, swagger_from_file='./swagger.yaml')
    return app


@routes.get('/task')
async def get_info(request):
    sa_session = ah_sa.get_session(request)
    query = request.rel_url.query
    # Check conditions
    if ut_common.REQUEST_UUID not in query:
        raise web.HTTPBadRequest(reason='Must send request date')
    if not query[ut_common.REQUEST_UUID]:
        raise web.HTTPBadRequest(reason='Empty request date')

    req_uuid = query[ut_common.REQUEST_UUID]
    async with sa_session.begin():
        statement = select(TableSchema.id, TableSchema.request_uuid).filter_by(request_uuid=req_uuid)
        try:
            result = await sa_session.execute(statement)
        except:
            raise
        compare_result = result.fetchall()
    return web.Response(text=f"request_uuid: {req_uuid}, id: {compare_result[0][0]}")


@routes.post('/task')
async def save_info(request):
    sa_session = ah_sa.get_session(request)
    query = request.rel_url.query
    # Check conditions
    if ut_common.ATTACHMENT_DEPTH not in query:
        raise web.HTTPBadRequest(reason='Must send attachment depth')
    if not query[ut_common.ATTACHMENT_DEPTH]:
        raise web.HTTPBadRequest(reason='Empty attachment depth')

    dt_str = query.get(ut_common.REQUEST_DATE, '')
    depth_level = int(query[ut_common.ATTACHMENT_DEPTH])
    req_uuid = str(uuid.uuid4())

    date_time = await ut_common.correct_form(dt_str)
    attachment = await ut_common.build_json_by_depth(depth_level)
    async with sa_session.begin():
        try:
            sa_session.add(TableSchema(request_uuid=req_uuid, request_date=date_time, attachment=attachment))
        except:
            await sa_session.rollback()
            raise
    data = {ut_common.REQUEST_UUID: req_uuid, ut_common.REQUEST_DATE: str(date_time), ut_common.ATTACHMENT: attachment}
    return web.json_response(data)


if __name__ == '__main__':
    web.run_app(app_start(), host="0.0.0.0")
