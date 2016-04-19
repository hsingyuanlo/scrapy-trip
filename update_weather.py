import json
from mysql_table import MysqlTaiwan, WeatherUpdateItem

json_file = open('./weather.json')
json_data = json.load(json_file)
json_file.close()


mysql = MysqlTaiwan()
for item in json_data:
    w_item = WeatherUpdateItem()
    w_item.id = item['id']
    w_item.temp_c = item['temp_c']
    w_item.pop = item['pop']
    mysql.update_weather(w_item)