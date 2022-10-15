import datetime
import unittest
from unittest.mock import patch
from johnnys_calendar import Event, Calendar


class TestJohnnysCalendar(unittest.TestCase):
    def test_is_lt(self):
        event1 = Event('event 1', '2022-10-15 13:00:00')
        later_dt = datetime.datetime.strptime('2022-10-17 13:00:00', '%Y-%m-%d %H:%M:%S')
        before_dt = datetime.datetime.strptime('2022-10-14 13:00:00', '%Y-%m-%d %H:%M:%S')
        same_dt = datetime.datetime.strptime('2022-10-15 13:00:00', '%Y-%m-%d %H:%M:%S')
        self.assertTrue(event1.is_lt(later_dt))
        self.assertFalse(event1.is_lt(before_dt))
        self.assertFalse(event1.is_lt(same_dt))

    @patch('johnnys_calendar.get_current_time')
    def test_process_events(self, mock_obj):
        mock_obj.return_value = datetime.datetime.strptime('2022-10-15 06:30:00', '%Y-%m-%d %H:%M:%S')
        db_path = './test_database.db'
        table_nm = 'calendar'
        calendar = Calendar(db_path=db_path, table_nm=table_nm)

        event1 = ('event1_kinpuri', '2022-10-15 05:30:00')
        event2 = ('event2_kinpuri', '2022-10-15 07:30:00')
        event3 = ('event3_kinpuri', '2022-10-15 08:30:00')
        event4 = ('event2', '2022-10-15 07:30:00')
        events = [event1, event2, event3, event4]

        event_text = calendar.process_events(events, filter_nm='abd')
        self.assertEqual('No more programs', event_text)

        event_text = calendar.process_events(events, filter_nm='kinpuri')
        expected = '''2022-10-15 07:30:00 - event2_kinpuri\n2022-10-15 08:30:00 - event3_kinpuri'''
        self.assertEqual(expected, event_text)


if __name__ == '__main__':
    unittest.main()
