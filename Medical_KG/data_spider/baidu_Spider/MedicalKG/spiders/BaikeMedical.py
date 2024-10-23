import scrapy
from scrapy import Selector
from scrapy_splash import SplashRequest
from ..items import MedicalkgItem
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re

scripts = """
            function main(splash, args)
                splash:go(args.url)
                splash:wait(args.wait)
                local cur_height = splash:evaljs("document.body.scrollTop")
                local scrollHeight = splash:evaljs("document.body.scrollHeight")
                local prev_height = 0
                local torrent = 10
                local lag_cnt = 0
                splash:set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
                while(cur_height < scrollHeight)
                do
                    splash:evaljs("window.scrollTo(0, document.body.scrollHeight)")
                    splash:wait(0.2)
                    prev_height = cur_height
                    cur_height = splash:evaljs("document.body.scrollTop")
                    splash:wait(0.1)
                    scrollHeight = splash:evaljs("document.body.scrollHeight")
                    splash:wait(0.1)
                    print(cur_height, scrollHeight)
                    if prev_height == cur_height then
                        lag_cnt = lag_cnt + 1
                        if lag_cnt == torrent then
                            break
                        end
                    end
                end
                return {
                    html = splash:html()
                }
            end
        """

class BaikemedicalSpider(scrapy.Spider):
    name = 'BaikeMedical'
    # allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/wikitag/taglist?tagId=75953']
                  # 'https://baike.baidu.com/wikitag/taglist?tagId=75954',
                  # 'https://baike.baidu.com/wikitag/taglist?tagId=75955',
                  # 'https://baike.baidu.com/wikitag/taglist?tagId=75956']
    triple_cnt = 0
    num_diseases = 0

    def parse_second_page(self, response):
        # page_target = response.xpath('//dl[@class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-"]/dd/h1/text()').extract_first()
        page_target = response.xpath('//dl[@class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-"]/dd/span[2]/h1/text()').extract_first()
        if page_target == None:
            page_target = response.xpath('//dl[@class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-"]/dd/span[1]/h1/text()').extract_first()
        blocks = response.xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]/dl')
        self.num_diseases += 1
        print(self.num_diseases)
        print(page_target)
        if page_target == None:
            print('here')
        for block in blocks:
            names = block.xpath('./dt/text()').extract()
            values = block.xpath('./dd/text()').extract()
            for name, value in zip(names, values):
                name = name.strip('\n').replace('\xa0', '').replace(' ', '')
                value = value.strip('\n').replace('\xa0', '').replace(' ', '')
                if len(value) == 0:
                    continue
                new_item = MedicalkgItem()
                new_item['head'] = page_target
                new_item['relation'] = name
                new_item['tail'] = value
                self.triple_cnt += 1
                if self.triple_cnt % 1000 == 0:
                    print(self.triple_cnt)
                yield new_item

    def parse(self, response):
        f = open('baike.baidu.com.txt')
        html = f.read()
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        url_units = soup.find_all('a', href=re.compile(r'/item/'))
        print(len(url_units))
        # print(response.text)
        for url_unit in url_units:
            url = url_unit['href']
            yield SplashRequest(url=url,
                                callback=self.parse_second_page,
                                )
