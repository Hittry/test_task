import datetime

import common as ut_common

from sqlalchemy import Column, DateTime, Integer, JSON, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TableSchema(Base):
    """ Схема данных для таблицы requests """

    __tablename__ = "requests"
    id = Column(ut_common.ID, Integer, primary_key=True, autoincrement=True)
    request_uuid = Column(ut_common.REQUEST_UUID, String(36), unique=True)
    request_date = Column(ut_common.REQUEST_DATE, DateTime, default=datetime.datetime.utcnow())
    attachment = Column(ut_common.ATTACHMENT, JSON)

    def __init__(self, request_uuid, request_date, attachment):
        self.request_uuid = request_uuid
        self.request_date = request_date
        self.attachment = attachment
