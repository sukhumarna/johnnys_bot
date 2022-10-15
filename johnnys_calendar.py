import datetime
from spider import JohnnysCrawler
from database import DatabaseManager


def get_current_time():
    return datetime.datetime.now()


class Event:
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    def is_lt(self, dt):
        return self.timestamp < dt


class Calendar:

    def __init__(self, db_path='./johnnys_database.db', table_nm='calendar'):
        self.db_manager = DatabaseManager(db_path=db_path, table_nm=table_nm)
        self.crawler = JohnnysCrawler()

    @staticmethod
    def process_events(events, filter_nm):
        curr_time = get_current_time()
        event_info = []
        print(f"process {len(events)} events")
        for event in events:
            event_obj = Event(name=event[0], timestamp=event[1])

            if (filter_nm != "" and filter_nm not in event[0]) | event_obj.is_lt(curr_time):
                continue
            event_info.append(f'{event[1]} - {event[0]}')
        if len(event_info) == 0:
            return 'No more programs'
        else:
            return '\n'.join(event_info)

    def get_calendar(self, filter_nm="平野紫耀"):
        events = self.db_manager.select_today_events()

        if len(events) < 1:
            # no current date data, fetch new data
            self.crawler.start_crawling()
            events = self.db_manager.select_today_events()

        # process events
        return self.process_events(events, filter_nm)
