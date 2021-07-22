import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from scrapy.selector import  Selector
import time
import csv
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

path = R"E:\Desktop\texas\chromedriver.exe"
a_list = []


class TxSpider(scrapy.Spider):
    name = 'TX'
    # allowed_domains = ['https://capitol.texas.gov/Reports/Report.aspx?LegSess=87R']
    # start_urls = ['http://https://capitol.texas.gov/Reports/Report.aspx?LegSess=87R/']
    def start_requests(self):
        urls = 'http://google.com'
        yield scrapy.Request(url=urls, callback=(self).parse)


    def parse(self, response):
        try:
            driver = webdriver.Chrome(path,options=chrome_options)
            driver.get("https://capitol.texas.gov/Reports/Report.aspx?LegSess=87R&ID=filedwogovsign")
            sel = Selector(text=driver.page_source)
            bill = sel.xpath("//tbody//td/a/text()").getall()
            # print(bill)
            time.sleep(2)
            links = sel.xpath("//tbody//td/a/@href").getall()
            with open(R"E:\Desktop\texas\out_3.csv", "w", newline="", encoding='utf8', ) as myfile:
                csv_writer = csv.writer(myfile, delimiter=",")
                for ur in links:
                    driver.get(ur)

                    button = driver.find_element_by_xpath('//div["pagetabs"]/a[@class="enabledButNotActive"][1]')
                    button.click()
                    time.sleep(1)
                    sel_1 = Selector(text=driver.page_source)
                    pdf = sel_1.xpath('//div[@id="content"][2]/form[@name="Form1"]/table[@width="95%"]//tr[last()]/td[2]/a[1]/@href').get()                    # csv_writer.writerow(pdf)
                    a_list.append("https://capitol.texas.gov"+pdf)
                for ln,mo in  zip(bill,a_list):
                    csv_writer.writerow([ln,mo])

                myfile.close()
                # print(a_list)
                # print(len(a_list))




            # print(links)
            # print("$$$$$$$$",len(links))
        except Exception as e:
            print("@@@@@@@@@@@@@",e)