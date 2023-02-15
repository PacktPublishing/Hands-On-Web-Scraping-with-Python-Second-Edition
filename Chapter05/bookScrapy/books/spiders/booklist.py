import scrapy
from books.items import BooksItem

class BooklistSpider(scrapy.Spider):
    name = "booklist"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    pageCount=0

    def parse(self, response):   
        
        listings = response.xpath("//article[@class='product_pod']") #root
        print("Books Count >> ", listings.__len__())   
        nextPage = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").extract_first()
        for listing in listings:
            
            column = BooksItem()
            
            column['url']=''
            column['title'] = listing.xpath(".//h3/a/@title[normalize-space()]").extract_first().strip()
            column['price'] = listing.xpath(".//div[2]/p[contains(@class,'price_color')]/text()").extract_first().strip()
            column['rating'] = listing.xpath(".//p[contains(@class,'star-rating')]/@class").extract_first().strip()
            column['stock'] = listing.xpath(".//div[2]/p[2][contains(@class,'availability')]/text()[normalize-space()]").extract_first().strip()
            column['url'] = listing.xpath(".//h3/a/@href").extract_first().strip()
            column['image'] = listing.xpath(".//div[1][contains(@class,'image_container')]/a/img/@src").extract_first().strip()
            
            #cleaning and formatting
            column['image'] = 'http://books.toscrape.com/'+column['image'].replace('../','').strip()
            column['rating'] = column['rating'].replace('star-rating','').strip()
            if column['url']:
                print(f"\n URL >> {column['url']}")                                  
                if 'catalogue' not in column['url']:
                    yield response.follow('http://books.toscrape.com/catalogue/'+column['url'],callback=self.parse_page, meta={'column':column})                
                else:
                    print(f"\n ----<<>")
                    yield response.follow('http://books.toscrape.com/'+column['url'],callback=self.parse_page, meta={'column':column})  
        
        #nextPage
        #nextPage = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").extract_first()
        if nextPage:# and self.pageCount<=3:
            nextPage = nextPage.replace('catalogue/','').strip()
            nextPage = 'http://books.toscrape.com/catalogue/'+nextPage
            print("Next Page URL: ",nextPage)
            self.pageCount+=1
            yield scrapy.Request(nextPage,callback=self.parse)
        
        print('Completed')

    def parse_page(self, response):
        print(f"inner page ")
        column = response.meta['column']
        column['category']=response.xpath("//ul[@class='breadcrumb']/li/a[contains(@href,'category')]/text()").extract()[-1]
        column['upc']=response.xpath("//table[1]/tr[1]/td[1]/text()").extract_first()
        column['no_review']=response.xpath("//table[1]/tr[last()]/td/text()").extract_first()      
        yield column
        