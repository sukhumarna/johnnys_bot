import datetime as dt
import scrapy
from scrapy.crawler import CrawlerProcess
from database import DatabaseManager


def is_today(date: str) -> bool:
    today = dt.date.today()
    month = int(date.split('/')[0])
    day = int(date.split('/')[1])
    if (today.month == month) & (today.day == day):
        return True
    else:
        return False


class JohnnysCrawler:

    @staticmethod
    def start_crawling(self):
        process = CrawlerProcess()
        process.crawl(JohnnysSpider)
        process.start()


class JohnnysSpider(scrapy.Spider):
    name = 'johnnys_calendar'

    def __init__(self, db_manager: DatabaseManager, *args, **kwargs):
        self.db_manager = db_manager
        super().__init__(*args, **kwargs)

    def start_requests(self):
        url = 'https://www.johnnys-net.jp/page?id=calendar'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        calendar_tabs = response.css('div.calendar-tab-content')

        date_list = response.xpath('//ul[contains(@class, "date-list")]')
        current_dt = date_list.css('li.date-list-item:nth-of-type(1) > a > span::text').extract_first()

        j_events = []
        if is_today(current_dt):
            print('check calendar is today: ', is_today(current_dt))
            curr_dt = dt.date.today()
            events = calendar_tabs[0].css('div.event-desc>dl')

            for event in events:
                event_dt = curr_dt
                event_detail = event.css('dd>p::text').extract()
                if len(event_detail) == 2:
                    continue
                else:
                    event_name = event_detail[2].strip()
                    event_time = event_detail[1].strip().split('-')[0]
                    event_hour = int(event_time.split(':')[0])
                    event_minute = int(event_time.split(':')[1])

                    if event_hour >= 24:
                        event_hour -= 24
                        event_dt = event_dt + dt.timedelta(days=1)

                    start_at = dt.datetime(year=event_dt.year, month=event_dt.month, day=event_dt.day,
                                           hour=event_hour, minute=int(event_minute))

                    j_events.append((event_name, start_at))
            print('insert johnny\'s events into the database')
            self.db_manager.insert_events(j_events)

        else:
            print('[ERROR] current date is', current_dt)

