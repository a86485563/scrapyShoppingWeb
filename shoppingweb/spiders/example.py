import scrapy
from scrapy import Request


from ..items import ShoppingwebItem


class ExampleSpider(scrapy.Spider):
    name = 'momospider'
    allowed_domains = ['m.momoshop.com.tw']
    # 將要爬的網址
    searchItem = 'iphone'
    start_pageIndex = 1
    start_url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage={}&searchType=1&cateLevel=2&ent=k&searchKeyword={}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(
            start_pageIndex, 'iphone')
    total_spider_page = 0
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    header = {'User-Agent': USER_AGENT}

    def start_requests(self):
        url = self.start_url
        # url = 'https://www.momoshop.com.tw/search/searchShop.jsp?keyword=iphone'
        # USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        # header = {'User-Agent': USER_AGENT}
        yield scrapy.Request(url=url, headers=self.header)

    def parse(self, response):

        self.logger.info('A response from %s just arrived!', response.url)
        #get current page
        strCurrentPage = response.css('div.pageArea>dl>dd.selected>a::text').extract_first()
        listPage = response.css('div.pageArea>dl>dd>a::text').extract()
        self.logger.info('strCurrentPage: %s', strCurrentPage)
        self.logger.info('listPage: %s', listPage)
        boolHaveNext = self.checkNextPage(strCurrentPage,listPage)
        self.logger.info('boolHaveNext: %s', boolHaveNext)

        for prdSelectior in response.css('li.goodsItemLi'):
            strStatus = prdSelectior.css('div.prdImgWrap').extract_first()
            # self.logger.info('strStatus %s',strStatus)
            boolStatus = not (strStatus.find('forsoldout')!=-1)
            self.logger.info('booStatus %s', str(boolStatus))
            yield {
                'name': prdSelectior.css('h3.prdName::text').extract_first(),
                'price': prdSelectior.css('div.prdInfoWrap > p.priceArea > span.priceSymbol > b.price::text').extract_first(),
                'link': prdSelectior.css('a::attr("href")').extract_first(),
                'status': boolStatus
            }
        if boolHaveNext:
            self.start_pageIndex = self.start_pageIndex +1
            next_page_url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage={}&searchType=1&cateLevel=2&ent=k&searchKeyword={}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(
                self.start_pageIndex, 'iphone')
            self.logger.info('intCurrentPage %s', self.start_pageIndex)
            self.logger.info('next_page_url %s',next_page_url)
            yield Request(next_page_url,headers=self.header,callback=self.parse,dont_filter=True)

        self.logger.info('finish')

    def checkNextPage(self,strCurrentPage:str,listPage:list):
        """checkNextPage(self,strCurrentPage: str,listPage:list) -> boolean is have next page or not"""

        self.logger.info("pageList %s",listPage)
        intNextPage = int(strCurrentPage)+1
        strNextPage = str(intNextPage)
        result = False
        if strNextPage in listPage:
            print(strCurrentPage, "found in list")
            result = True
        else:
            print(strCurrentPage, "not present in list")

        return result
