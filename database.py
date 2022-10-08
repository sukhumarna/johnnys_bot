import sqlite3
from sqlite3 import Error


class DatabaseManager:
    def __init__(self, db_path, table_nm):
        self.db_path = db_path
        self.table_name = table_nm
        self.conn = None

        print('create connection...')
        self._create_connection()

        print('create table if not exists')
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

    def insert_events(self, events):
        sql = f''' INSERT INTO {self.table_name}(name,start_at)
                            VALUES(?,?) '''
        cur = self.conn.cursor()
        for event in events:
            cur.execute(sql, event)
        self.conn.commit()

    def close(self):
        self.conn.close()


# db = DatabaseManager(db_path='./johnnys_database.db', table_nm='calendar')
# db.insert_event((
#     'Kurosaku',
#     dt.datetime(year=2022, month=10, day=22,
#                 hour=22, minute=0)
# ))
# db.conn.commit()
# db.conn.close()

