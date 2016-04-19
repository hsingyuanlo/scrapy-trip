import json

from scrapy.spider import Spider
from scrapy.selector import Selector
from trip.items import ViewItem


class ViewSpiderSpider(Spider):
    name = "view_spider"
    allowed_domains = ["taiwan.net.tw"]

    def __init__(self):
        self.start_urls, self.name_map, self.county_map, self.category_map = read_data_from_county_view_url()
        self.log_file = open('./log.txt', 'w')

    def __del__(self):
        self.log_file.close()

    def parse(self, response):
        try:
            url = response.url
            sel = Selector(response)
            items = sel.xpath('//table[@id="ctl00_ContentPlaceHolder1_Wuc_Cnt1_Wuc_OneView1_objTbe"]/tr')

            contact = None
            address = None
            coordinate = None

            for item in items:
                title = item.xpath('th/text()')[0].extract()
                if title == u'\u96fb\u8a71':
                    contact = item.xpath('td/text()')
                    if len(contact) > 0:
                        contact = contact[0].extract()
                elif title == u'\u5730\u5740':
                    address = item.xpath('td/span/text()')
                    if len(address) > 0:
                        address = address[0].extract()
                    else:
                        address = None

                    coordinate = item.xpath('td/span/div/text()')
                    if len(coordinate) > 0:
                        coordinate = coordinate[0].extract()
                    else:
                        coordinate = None

            f_name = self.name_map[url]
            f_county = self.county_map[url]
            f_category = self.category_map[url]
            f_contact= contact
            f_address = address
            f_latitude, f_longitude = process_coordinate_info(coordinate)

            i = ViewItem()
            i['name'] = f_name
            i['county'] = f_county
            i['category'] = f_category
            i['contact'] = f_contact
            i['address'] = f_address
            i['latitude'] = float(f_latitude)
            i['longitude'] = float(f_longitude)
            return i
        except:
            self.log_file.write('ERROR: {0}\n'.format(url))

# read json data output from previous command
def read_data_from_county_view_url():
    json_file = open('./county_view_url.json')
    json_data = json.load(json_file)
    json_file.close()

    url_list = list()
    url_name_map = dict()
    url_county_map = dict()
    url_category_map = dict()

    for json_item in json_data:
        name = json_item['name']
        county = json_item['county']
        category = json_item['category']
        link = json_item['link']

        url_list.append(link)
        url_name_map[link] = name
        url_county_map[link] = county
        url_category_map[link] = category

    return ['http://taiwan.net.tw/m1.aspx?sNo=0001114&id=3275'],\
           url_name_map, url_county_map, url_category_map


# separate coordinate into latitude and longitude
def process_coordinate_info(coordinate):
    if coordinate is None:
        return -1, -1
    coordinate = coordinate.replace(u'\u7d93\u5ea6/\u7def\u5ea6\xa0\xa0', '').replace('(', '').replace(')', '')
    temp = coordinate.split(',')
    r_latitude = temp[0]
    r_longitude = temp[1]
    return r_latitude, r_longitude