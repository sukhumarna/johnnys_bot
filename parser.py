import datetime as dt
from scrapy import Selector


def is_today(date: str) -> bool:
    today = dt.date.today()
    month = int(date.split('/')[0])
    day = int(date.split('/')[1])
    if (today.month == month) & (today.day == day):
        return True
    else:
        return False


with open('./johnnys_calendar.html', 'r') as f:
    html_string = f.read()

sel = Selector(text=html_string)

calendar_tabs = sel.css('div.calendar-tab-content')

date_list = sel.xpath('//ul[contains(@class, "date-list")]')
current_dt = date_list.css('li.date-list-item:nth-of-type(1) > a > span::text').extract_first()

print('check calendar is today: ', is_today(current_dt))

events = calendar_tabs[0].css('div.event-desc>dl')
curr_dt = dt.date.today()

j_events = []

for event in events:
    event_dt = curr_dt
    event_detail = event.css('dd>p::text').extract()
    # contents = event_detail.split(',')
    if len(event_detail) == 2:
        event_time = 'NA'
        event_name = event_detail[-1].strip()
    else:
        event_name = event_detail[2].strip()
        event_time = event_detail[1].strip().split('-')[0]
        print(f'{event_name} start at {event_time}')

        event_hour = int(event_time.split(':')[0])
        event_minute = int(event_time.split(':')[1])

        if event_hour >= 24:
            event_hour -= 24
            event_dt = curr_dt + dt.timedelta(days=1)

        start_at = dt.datetime(year=event_dt.year, month=event_dt.month, day=event_dt.day,
                               hour=event_hour, minute=int(event_minute))

        j_events.append((event_name, start_at))



print(j_events)





