import scrapy


class BarnesandnobleSpiderSpider(scrapy.Spider):
    name = 'barnesandnoble_spider'
    allowed_domains = ['barnesandnoble.com']
    start_urls = ['http://barnesandnoble.com/']
    proxy = "192.168.1.199:7890"

    def start_requests(self):
        for page in range(1,48):
            yield scrapy.Request("https://www.barnesandnoble.com/b/50-off-criterion-collection/_/N-2vtrZ1f?Nrpp=20&page=" + str(page),
                                method="GET",
                                meta={"proxy": self.proxy},
                                callback=self.parse)
    def parse(self, response):
        if(response.url.find('page') > 0):
            results = response.css('.pImageLink::attr(href)').getall()
            yield from response.follow_all(results, meta={"proxy": self.proxy})
        else:
            title = response.css('#prodSummary-header .pdp-header-title::text').get()
            category = response.css('.formatSelect a p::text').getall()
            price = response.css('.format-price strong::text').getall()
            dic = dict(zip(category,price))
            yield {
                'path':response.url,
                'title':title,
                'price':dic
            }