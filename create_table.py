__author__ = 'hylo'

import json
import re

from mysql_table import MysqlTaiwan
from mysql_table import AttractionItem, LocationItem, WeatherItem

# read files
json_file = open('./view_info.json')
view_data = json.load(json_file)
json_file.close()

json_file = open('./location_info.json')
location_data = json.load(json_file)
json_file.close()

# Construct in-memory data structure
weather_list = list()
weather_key_map = dict()
for i, j in enumerate(location_data, 1):
    w_item = WeatherItem()
    w_item.id = i
    w_item.key = j['id']
    weather_list.append(w_item)
    weather_key_map[j['id']] = i

location_list = list()
location_name_map = dict()
number_map = dict()
for i, j in enumerate(location_data, 1):
    number_map[j['id']] = i

for i in location_data:
    l_item = LocationItem()
    l_item.id = number_map[i['id']]
    l_item.name = i['name']
    l_item.ref_location_id = number_map.get(i['pid'])
    l_item.ref_weather_id = weather_key_map.get(i['id'])
    location_list.append(l_item)
    location_name_map[i['name']] = l_item

attraction_list = list()
for i, j in enumerate(view_data, 1):
    a_item = AttractionItem()
    a_item.id = i
    a_item.name = j['name']
    a_item.county = j['county']
    a_item.category = j['category']
    a_item.contact = j['contact']
    a_item.address = j['address']
    a_item.latitude = j['latitude']
    a_item.longitude = j['longitude']
    attraction_list.append(a_item)

# Map Attraction.ref_location_id to Location.id
location_id_map = dict()
for a_item in attraction_list:
    address = a_item.address
    county = a_item.county

    # find county info from map
    county = re.sub('\(.*\)', '', county)
    l_item = location_name_map.get(county)
    l_id = l_item.id

    # find town info from map
    town_list = location_id_map.get(l_id)

    # If not found, generate one, add into map
    if town_list is None:
        town_list = [x for x in location_list if x.ref_location_id == l_id]
        location_id_map[l_id] = town_list

    # map address to town id
    town_id = None
    for t in town_list:
        if t.name in address:
            town_id = t.id
            break
    a_item.ref_location_id = town_id

# Build MySQL data
db = MysqlTaiwan()
db.create_table()

for item in location_list:
    db.insert_location(item)

for item in weather_list:
    db.insert_weather(item)

for item in attraction_list:
    db.insert_attraction(item)