import spider
from scrapy.crawler import CrawlerProcess


def main():
    process = CrawlerProcess()
    process.crawl(spider.JohnnysSpider)
    process.start()


if __name__ == '__main__':
    main()
