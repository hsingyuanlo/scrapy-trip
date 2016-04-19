import json
from scrapy.spider import Spider
from scrapy.selector import Selector
from trip.items import CountyViewUrlItem


class CountyViewUrlSpider(Spider):
    name = "county_view_url"
    allowed_domains = ["www.taiwan.net.tw"]
    base_url = 'http://taiwan.net.tw/'

    def __init__(self):
        self.start_urls, self.url_map = read_data_from_county_url()
        pass

    def parse(self, response):
        sel = Selector(response)
        url = response.url
        main = sel.xpath('//table[@id="ctl00_ContentPlaceHolder1_Wuc_Cnt1_Wuc_View1_1_TbeObject"]/tr/td')
        ret = list()

        county = self.url_map.get(url)
        category = None
        for item in main:
            i = CountyViewUrlItem()
            categories = item.xpath('span/text()')
            if len(categories) > 0:
                category = categories[0].extract()
            else:
                name = item.xpath('a/text()')[0].extract()
                link = '{0}{1}'.format(self.base_url, item.xpath('a/@href')[0].extract())
                i['name'] = name
                i['county'] = county
                i['category'] = category
                i['link'] = link
                ret.append(i)

        return ret

def read_data_from_county_url():
    json_file = open('./county_url.json')
    json_data = json.load(json_file)
    json_file.close()

    url_map = {}
    url_list = []

    for json_item in json_data:
        link = json_item['link']
        name = json_item['name']
        url_list.append(link)
        url_map[link] = name

    return url_list, url_map