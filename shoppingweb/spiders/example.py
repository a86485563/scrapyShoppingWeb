import scrapy


from ..items import ShoppingwebItem


class ExampleSpider(scrapy.Spider):
    name = 'momospider'
    allowed_domains = ['momoshop.com']
    # 將要爬的網址
    searchItem = 'iphone'

    def start_requests(self):
        url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage={}&searchType=1&cateLevel=2&ent=k&searchKeyword={}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(
            1, 'iphone')
        # url = 'https://www.momoshop.com.tw/search/searchShop.jsp?keyword=iphone'
        USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        header = {'User-Agent': USER_AGENT}
        yield scrapy.Request(url=url, headers=header)

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        # self.logger.info(response.body)
        # for prodInfo in response.xpath('//div[@id="prdInfoWrap"]/text()').extract() :
        #     self.logger.info('prodInfo : ', prodInfo)
        # self.logger.info(response.xpath('//li[contains(@class, "goodsItemLi")]').getall())
        for prdSelectior in response.xpath('//li[contains(@class, "goodsItemLi")]'):
            yield {
                'name': prdSelectior.xpath('//a//div[@class = "prdInfoWrap"]//h3[@class = "prdName"]/text()').extract_first()
            }

        self.logger.info('finish')
