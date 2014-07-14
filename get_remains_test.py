#! /usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
from selenium import webdriver
from models import *
from suds.client import Client



class GetRemainsTest(unittest.TestCase):
    
    SITE = 'http://nsk.%s/' % os.getenv('SITE')
    WSDL = os.getenv('WSDL')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    SCHEMA = os.getenv('SCHEMA')
    USER = os.getenv('USER')
    PSWD = os.getenv('PSWD')
    driver = webdriver.Firefox()
    CONNECT_STRING = 'mysql://%s:%s@%s:%s/%s?charset=utf8' %(USER, PSWD, HOST, PORT, SCHEMA)
    engine = create_engine(CONNECT_STRING, echo=False) #Значение False параметра echo убирает отладочную информацию
    metadata = MetaData(engine)
    session = create_session(bind = engine)

    

    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""

        if sys.exc_info()[0]:   
            print sys.exc_info()[0]

    def check_remains(self, members):
        """ Проверяет остатки и возвращает количество ошибок """
        errors = 0
        
        for item in members:

            if item.ShopCode[:3] in ('021', 'B19', '067', '034', '035',
                                     '036', '037', '038', '039', '006'):
                continue

            #проверяем есть ли магазин в БД сайта, если есть берем значение поля db_sort_field
            store_shop = self.session.query(Shops.db_sort_field).filter(Shops.scode == item.ShopCode[:3]).first()
            if store_shop != None:
                store_shop = store_shop[0]
            else:
                cnt += 1
                print 'Нужный магазин не найден в БД'
                print 'Код магазина в 1С - ', item.ShopCode[:3]
                print '*'*80
                continue

            #проверяем есть ли товар в БД сайта, если есть берем значение поля id  
            goods_id = self.session.query(Goods.id).filter(Goods.pcode == item.Code).first()
            if goods_id != None:
                goods_id = goods_id[0]
            else:
                cnt += 1
                print 'Нужный товар не найден в БД'
                print 'Код товара в 1С - ', item.Code
                print '*'*80
                continue

            #узнаем остаток конкретного товара в конкретном магазине    
            query_result = self.engine.execute('SELECT t_goods_remains.%s FROM t_goods_remains WHERE goods_id=%s;' % (store_shop, goods_id)).fetchone()[0]

            #сравниваем с данными из 1С
            if query_result != item.Quantity:
                cnt += 1
                print 'Ошибка в количестве товара:'
                print 'Код товара в 1С - ', item.Code, ' / ', 'Код магазина из 1С - ', item.ShopCode[:3]
                print 'Количество с вебсервиса - ', int(item.Quantity)
                print 'Количество из базы сайта - ', query_result
                print '*'*80

        return errors

        

    def test_get_remains(self):
        """ Выполняет процедуру из браузера и парсит страницу на наличие ответа """
        correct = True # Test status: True - runs well, False - an error occurred
        self.driver.get('%slogin' % self.SITE)
        
        self.driver.find_element_by_id('username').send_keys(os.getenv('AUTH'))
        self.driver.find_element_by_id('password').send_keys(os.getenv('AUTHPASS'))
        self.driver.find_element_by_class_name('btn-primary').click()
        
        self.driver.get('%sterminal/maintenance/5' % self.SITE)
        status = self.driver.find_elements_by_tag_name('div')[1]
        self.driver.get_screenshot_as_file('maintenance_result.png')
        if '2' not in status.text:
            correct = False
            print 'Процедура завершилось с ошибкой, подробности можно посмотреть на скриншоте'
            print status.text
            assert correct, (u'Maintenance was finished with error')
        self.driver.get('%slogout/' % self.SITE)
        self.driver.close()

        wsdl_url = self.WSDL
        client = Client(wsdl_url) #подключаемся к вебсервису

        #создаем новый тип для общения с вебсервисом
        parameters = client.factory.create('ns1:ParameterRemainderProducts')
        """(ParameterRemainderProducts){
               AllShops = None
               FilterByShops[] = <empty>
               AllProducts = None
               FilterByProducts[] = <empty>
               FilterByProductsCode[] = <empty>
             }"""
        #задаем свойства объекта, выступают в роли параметров
        parameters.AllShops = True
        parameters.FilterByShops = ''
        parameters.AllProducts = True
        parameters.FilterByProducts = ''
        parameters.FilterByProductsCode = ''
        
        response = client.service.GetRemainderProducts(parameters)
        
        cnt = check_remains(response.Members)
                
        assert cnt==0, (u'Errors found: %d')%(cnt)
