import scrapy
from scrapy.http import Request
class TxSpider(scrapy.Spider):
    name = 'TX'
    # allowed_domains = ['capitol.texas.gov']
    start_urls = ['https://capitol.texas.gov/Reports/Report.aspx?LegSess=87R&ID=filedwogovsign']
    def parse(self, response):
        url = response.xpath('//table//tr/td/a/@href').extract()
        for i in url:
            yield Request(url=i,callback=self.parse_more)

    def parse_more(self,response):
        next_url = response.xpath('//div[@id="pagetabs"]/a[2]/@href').extract_first()
        ab_url = "https://capitol.texas.gov/BillLookup/" + next_url
        yield Request(url=ab_url,callback=self.parse_next)

    def parse_next(self,response):
        bill_no = response.xpath('//div[@id="content"]//td//td[2]/span/text()').extract_first()
        status = response.xpath('//table[@border="0"][@cellpadding="5"][1]//tr[last()]/td/text()[1]').extract_first()
        url = response.xpath('//table[@border="0"][@cellpadding="5"][1]//tr[last()]/td[2]/a[1]/@href').extract_first()
        url = "https://capitol.texas.gov/" + url
        yield {
            'bill no. ': bill_no,
            'status' : status,
            'url': url
        }



