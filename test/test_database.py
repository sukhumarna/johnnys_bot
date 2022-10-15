import datetime as dt
import unittest
from database import DatabaseManager


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.table_nm = 'calendar'
        db_manager = DatabaseManager(db_path='./test_database.db', table_nm=cls.table_nm)
        cls.db_manager = db_manager

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db_manager.close()

    def tearDown(self) -> None:
        cur = self.db_manager.conn.cursor()
        del_sql = f'DELETE FROM {self.table_nm}'
        cur.execute(del_sql)
        self.db_manager.conn.commit()

    def test_insert_events(self):
        events = []
        event_dt = dt.date.today()
        events.append(("event1", dt.datetime(year=event_dt.year, month=event_dt.month, day=event_dt.day,
                                             hour=5, minute=30)))
        events.append(("event2", dt.datetime(year=event_dt.year, month=event_dt.month, day=event_dt.day,
                                             hour=15, minute=45)))
        self.db_manager.insert_events(events)

        sql = f'SELECT * FROM {self.table_nm}'
        cur = self.db_manager.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        self.assertEqual(2, len(rows))

    def test_select_today_events(self):
        events = []
        event_dt = dt.date.today()
        events.append(("event1", dt.datetime(year=event_dt.year, month=event_dt.month, day=event_dt.day,
                                             hour=5, minute=30)))
        event_tmr = event_dt + dt.timedelta(days=1)
        events.append(("event2", dt.datetime(year=event_tmr.year, month=event_tmr.month, day=event_tmr.day,
                                             hour=15, minute=45)))
        event_ysd = event_dt - dt.timedelta(days=1)
        events.append(("event2", dt.datetime(year=event_ysd.year, month=event_ysd.month, day=event_ysd.day,
                                             hour=22, minute=45)))
        self.db_manager.insert_events(events)

        events = self.db_manager.select_today_events()
        self.assertEqual(1, len(events))


if __name__ == '__main__':
    unittest.main()
