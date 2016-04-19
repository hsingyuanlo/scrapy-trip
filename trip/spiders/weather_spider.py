from datetime import datetime
from dateutil import parser
from dateutil.tz import tzlocal
from scrapy.contrib.spiders import XMLFeedSpider
from trip.items import WeatherItem


class LocationSpider(XMLFeedSpider):
    name = 'weather'
    allowed_domains = ['http://opendata.cwb.gov.tw/']
    start_urls = [
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-001.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-005.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-009.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-013.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-017.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-021.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-025.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-029.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-033.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-037.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-041.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-045.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-049.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-053.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-057.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-061.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-065.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-069.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-073.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-077.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-081.xml',
        'http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-085.xml'
    ]

    iterator = 'xml' # you can change this; see the docs
    itertag = 'location' # change it accordingly

    def __init__(self):
        self.current_url = None
        self.url_map = dict()

    def parse_node(self, response, selector):
        url = response.url

        i = WeatherItem()
        i['id'] = selector.xpath('@id')[0].extract()

        # now datetime
        now_time = datetime.now().replace(tzinfo=tzlocal())

        # temp_c
        t_list = selector.xpath('weather-elements/T/time')
        i['temp_c'] = None
        if len(t_list) > 0:
            gt_time = now_time
            gt_value = None
            for t_item in t_list:
                time = t_item.xpath('@at')[0].extract()
                obj_time = parser.parse(time)
                value = clean_text(t_item.xpath('value/text()')[0].extract())
                if (gt_value is None and obj_time >= now_time) or gt_time >= obj_time >= now_time:
                    gt_time = obj_time
                    gt_value = value
            i['temp_c'] = gt_value

        # pop
        pop_list = selector.xpath('weather-elements/PoP/time')
        i['pop'] = None
        if len(pop_list) > 0:
            pop_value = None
            for pop_item in pop_list:
                s_time = parser.parse(pop_item.xpath('@start')[0].extract())
                e_time = parser.parse(pop_item.xpath('@end')[0].extract())
                value = clean_text(pop_item.xpath('value/text()')[0].extract())
                if (pop_value is None) or s_time >= now_time >= e_time:
                    pop_value = value
            i['pop'] = pop_value

        return i


def clean_text(txt):
    return txt.replace('\n', '').replace(' ', '')
