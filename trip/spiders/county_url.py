from scrapy.spider import Spider
from scrapy.selector import Selector
from trip.items import CountyUrlItem


class CountyUrlSpider(Spider):
    name = "county_url"
    allowed_domains = ["www.taiwan.net.tw"]
    start_urls = (
        'http://taiwan.net.tw/m1.aspx?sNo=0001016',
        )
    base_url = 'http://taiwan.net.tw/'

    def parse(self, response):
        sel = Selector(response)
        ret = list()

        view_list = sel.xpath('//div[@class="sport_view"]/a')

        for view in view_list:
            i = CountyUrlItem()
            i['name'] = view.xpath('text()')[0].extract()
            i['link'] = "{0}{1}".format(self.base_url, view.xpath('@href')[0].extract())
            ret.append(i)

        return ret