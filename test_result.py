__author__ = 'hylo'

import json

json_file = open('./county_view_url.json')
county_view_url_json = json.load(json_file)
json_file.close()

json_file = open('./view_info.json')
view_info_json = json.load(json_file)
json_file.close()

name_map = dict()
name_map_removed = dict()

print('=========================================')
print('Total count in county_view_url_json is {0}'.format(len(county_view_url_json)))
print('=========================================')
for item in county_view_url_json:
    name = item['name']
    county = item['county']
    name_map[(name, county)] = item

print('=========================================')
print('Total count in view_info_json is {0}'.format(len(view_info_json)))
print('=========================================')
for item in view_info_json:
    name = item['name']
    county = item['county']
    if (name, county) in name_map_removed.keys():
        temp = name_map_removed.get((name, county))
        print('Duplicate: {0} {1}\n'.format(name.encode('utf-8'), county.encode('utf-8')))

    j_item = name_map.get((name, county))
    if j_item is not None:
        name_map.pop((name, county))
        name_map_removed[(name, county)] = j_item


print('=========================================')
print('Miss {0} data'.format(len(name_map)))
print('=========================================')
for item in name_map.keys():
    print name_map[item]
