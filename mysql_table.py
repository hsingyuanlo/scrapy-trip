__author__ = 'hylo'

import MySQLdb


class AttractionItem:
    def __init__(self):
        self.id              = None
        self.name            = None
        self.category        = None
        self.contact         = None
        self.address         = None
        self.latitude        = None
        self.longitude       = None
        self.ref_location_id = None
        self.county          = None


class LocationItem:
    def __init__(self):
        self.id              = None
        self.name            = None
        self.ref_location_id = None
        self.ref_weather_id  = None


class WeatherItem:
    def __init__(self):
        self.id     = None
        self.temp_c = None
        self.pop    = None
        self.key    = None


class WeatherUpdateItem:
    def __init__(self):
        self.id     = None
        self.temp_c = None
        self.pop    = None


def print_msg(desc, msg):
    if msg is not None:
        if type(msg) == unicode:
            print desc, ':', msg.encode('utf-8')
        else:
            print desc, ':', msg
    else:
        print desc, ': None'


def print_a_msg(item):
    print('===========')
    print_msg('id', item.id)
    print_msg('name', item.name)
    print_msg('category', item.category)
    print_msg('contact', item.contact)
    print_msg('address', item.address)
    print_msg('latitude', item.latitude)
    print_msg('longitude', item.longitude)
    print_msg('county', item.county)
    print_msg('ref_location_id', item.ref_location_id)


def print_l_msg(item):
    print('===========')
    print_msg('id', item.id)
    print_msg('name', item.name)
    print_msg('ref_location_id', item.ref_location_id)
    print_msg('ref_weather_id', item.ref_weather_id)


def print_w_msg():
    pass


def test_null(item):
    if item is not None:
        if isinstance(item, unicode):
            return '\'{0}\''.format(item.encode('utf-8'))
        else:
            return item
    return 'null'


class MysqlTaiwan:

    def __init__(self):
        self.debug = True
        # Set up your connection information
        self.conn = MySQLdb.connect(host='localhost', user='opendata', passwd='p@ssw0rd', db='about_taiwan', charset='utf8')

    def __del__(self):
        self.conn.close()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('create table location'
                  '('
                  '    id int not null,'
                  '    name varchar(255) character set utf8 not null,'
                  '    ref_location_id integer,'
                  '    ref_weather_id integer,'
                  '    primary key (id)'
                  ');')
        c.execute('create table weather'
                  '('
                  '    id integer not null,'
                  '    temp_c int,'
                  '    pop int,'
                  '    w_key char(10) not null,'
                  '    primary key (id)'
                  ');')
        c.execute('create table attraction'
                  '('
                  '    id int not null,'
                  '    name varchar(255) character set utf8 not null,'
                  '    category varchar(255) character set utf8 not null,'
                  '    contact varchar(255) character set utf8,'
                  '    address varchar(255) character set utf8,'
                  '    latitude float,'
                  '    longitude float,'
                  '    ref_location_id int not null'
                  ')')

    def drop_table(self):
        c = self.conn.cursor()
        c.execute('drop table location')
        c.execute('drop table weather')
        c.execute('drop table attraction')

    def insert_location(self, item):
        if isinstance(item, LocationItem):
            c = self.conn.cursor()
            c.execute('insert into location values({0}, \'{1}\', {2}, {3})'
                      .format(item.id,
                              item.name.encode('utf-8'),
                              test_null(item.ref_location_id),
                              item.ref_weather_id))
            self.conn.commit()

    def insert_weather(self, item):
        if isinstance(item, WeatherItem):
            c = self.conn.cursor()
            c.execute('insert into weather values({0}, {1}, {2}, \'{3}\')'
                      .format(item.id,
                              test_null(item.temp_c),
                              test_null(item.pop),
                              item.key))
            self.conn.commit()

    def insert_attraction(self, item):
        if isinstance(item, AttractionItem):
            c = self.conn.cursor()
            c.execute('insert into attraction values({0}, \'{1}\', \'{2}\', {3}, \'{4}\', {5}, {6}, {7})'
                      .format(item.id,
                              item.name.encode('utf-8'),
                              item.category.encode('utf-8'),
                              test_null(item.contact),
                              item.address.encode('utf-8'),
                              item.latitude,
                              item.longitude,
                              int(item.ref_location_id)))
            self.conn.commit()

    def update_weather(self, item):
        if isinstance(item, WeatherUpdateItem):
            c = self.conn.cursor()
            c.execute('update weather set temp_c={0}, pop={1} where w_key=\'{2}\''
                      .format(test_null(item.temp_c),
                              test_null(item.pop),
                              item.id))
            self.conn.commit()
