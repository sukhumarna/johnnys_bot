import datetime as dt
import logging
import sqlite3
from sqlite3 import Error


class DatabaseManager:
    def __init__(self, db_path, table_nm):
        self.db_path = db_path
        self.table_name = table_nm
        self.conn = None

        logging.info('create connection...')
        self._create_connection()

        logging.info('create table if not exists')
        self._create_table()

    def _create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
        except Error as e:
            print(e)
        self.conn = conn

    def _create_table(self):
        # Drop table
        drop_sql = f"""
                    DROP TABLE IF EXISTS {self.table_name};
                    """
        # Creating table
        create_sql = f""" CREATE TABLE IF NOT EXISTS {self.table_name} (
                    name text NOT NULL,
                    start_at datetime NOT NULL
                );"""
        try:
            c = self.conn.cursor()
            c.execute(drop_sql)
            c.execute(create_sql)
        except Error as e:
            print(e)

    def select_all_events(self):
        sql = f'SELECT * FROM {self.table_name}'
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def insert_events(self, events):
        sql = f''' INSERT INTO {self.table_name}(name,start_at)
                            VALUES(?,?) '''
        cur = self.conn.cursor()
        for event in events:
            cur.execute(sql, event)
        self.conn.commit()

    def select_today_events(self):
        today = dt.date.today()  #.strftime('%Y-%m-%d')
        logging.info(f'current date is {today}')
        # sql = f'''
        #         SELECT * FROM {self.table_name}
        #         WHERE DATE(start_at) = {today}'''
        sql = f"""SELECT * FROM {self.table_name} WHERE DATE(start_at) = ?"""

        cur = self.conn.cursor()
        cur.execute(sql, (today,))
        rows = cur.fetchall()
        return rows

    def close(self):
        self.conn.close()

