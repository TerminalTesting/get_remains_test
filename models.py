#! /usr/bin/python
# -*- coding: utf8 -*-
""" объекты для работы с БД """

# from sqlalchemy import *
# from sqlalchemy.orm import create_session, relationship
# from sqlalchemy.orm.mapper import Mapper
# from sqlalchemy.orm import mapper
# from sqlalchemy import Column
# from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import Column, Integer, Unicode, String, Float
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session

Base = declarative_base()

class Goods( Base ):
    """ Товары """
    __tablename__ = 't_goods'
    id=Column( Integer, primary_key=True)
    alias=  Column( Unicode)
    block_id=Column( Integer, ForeignKey('t_goods_block.id') )
    overall_type=Column( Integer)
    pcode = Column( Unicode )

class Goods_stat( Base ):
    """ Статусы товара"""
    __tablename__="t_goods_cities"#, metadata,
    city_id=Column( Integer, ForeignKey('t_cities.id'), primary_key=True)
    goods_id=Column( Integer, ForeignKey('t_goods.id'), primary_key=True)
    status=Column( Integer)

class Goods_block( Base ):
    """ Название инф.блоков"""
    __tablename__='t_goods_block'
    id=Column( Integer, primary_key=True )
    flag_self_delivery=Column( Integer )
    name=Column( Unicode )
    delivery_type=Column( Integer )

class Region( Base ):
    """ Регионы """
    __tablename__="t_cities"#, metadata,
    id=Column(Integer, primary_key=True)
    name=Column( Unicode)
    domain=Column( Unicode)
    price_type_guid=Column( String())
    supplier_id = Column( Integer )

class Shops( Base ):
    """Магазины региона"""
    __tablename__="t_shops"#, metadata,
    id=Column(Integer, primary_key=True)
    active = Column(Integer)
    city_id=Column(Integer, ForeignKey('t_cities.id'))
    flag_no_self_delivery_kbt = Column( Integer)
    flag_no_self_delivery = Column( Integer)
    flag_store_shop = Column( Integer)
    flag_store_shop_kbt = Column( Integer)
    db_sort_field = Column( Unicode )
    scode = Column( Unicode )

class Remains( Base ):
    __tablename__="t_goods_remains"#, metadata,
    goods_id = Column(Integer, ForeignKey('t_goods.id'), primary_key=True )

class Goods_price( Base ):
    """ Цены товара """
    __tablename__='t_goods_prices'#, metadata,
    price_type_guid=Column( String(), primary_key=True )
    goods_id =Column(Integer, primary_key=True)
    price=Column(Float)
    price_supplier=Column(Float)
     
class Additional( Base ):
    """ Доп. услуги к товару """
    __tablename__= 't_goods_block_additional'
    goods_id=Column( Integer, ForeignKey('t_goods_block.id'), primary_key=True)
    block_id=Column( Integer, primary_key=True)

class Warranty( Base ):
    """ Доп. гарантия к товару """
    __tablename__= 't_goods_block_warranty'
    goods_id=Column( Integer, ForeignKey('t_goods_block.id'), primary_key=True)
    block_id=Column( Integer, primary_key=True)
        
