from scrapy.contrib.spiders import XMLFeedSpider
from trip.items import LocationItem

class LocationSpider(XMLFeedSpider):
    name = 'location'
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

        i = LocationItem()
        i['id'] = selector.xpath('@id')[0].extract()
        i['name'] = clean_text(selector.xpath('name/text()')[0].extract())

        if len(i['id']) == 5 or len(i['id']) == 4:
            self.url_map[url] = i['id']
            i['pid'] = None
        else:
            i['pid'] = self.url_map.get(url)

        return i

def clean_text(txt):
    return txt.replace('\n', '').replace(' ', '')
