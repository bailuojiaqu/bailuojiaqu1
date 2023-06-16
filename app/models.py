# coding: utf-8
from sqlalchemy import Column, Float, Integer, String, text
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomMonth(Base):
    __tablename__ = 'custom_month'

    id = Column(Integer, primary_key=True, nullable=False)
    customname = Column(String(255, 'utf8mb4_general_ci'), primary_key=True, nullable=False)
    month = Column(Integer, nullable=False)
    is_del = Column(Integer, nullable=False, server_default=text("'0'"))
    datetime = Column(DATETIME(fsp=6))


class CustomName(Base):
    __tablename__ = 'custom_name'

    id = Column(Integer, primary_key=True, nullable=False)
    custom_name = Column(String(255, 'utf8mb4_general_ci'), primary_key=True, nullable=False)
    is_del = Column(Integer, nullable=False, server_default=text("'0'"))
    datetime = Column(DATETIME(fsp=6))


class FormTotal(Base):
    __tablename__ = 'form_total'

    id = Column(Integer, primary_key=True, nullable=False)
    customname = Column(String(255, 'utf8mb4_general_ci'), primary_key=True, nullable=False)
    year = Column(Integer, nullable=False)
    date = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    size = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    num = Column(Integer, nullable=False)
    price = Column(Float(10), nullable=False)
    price_total = Column(Integer, nullable=False)

