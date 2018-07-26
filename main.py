import sys
import sqlite3
from datetime import date
from hardware import ArduinoConn, SENSORS_NUMBER

SQL_CREATE_TABLE = """
    CREATE TABLE sensors (
        temperature1 real,
        temperature2 real,
        pressure real
    )
"""
SQL_INSERT = """
    INSERT INTO sensors VALUES (?, ?, ?) 
"""


class DataServer:

    def __init__(self):
        self.arduino = ArduinoConn(sys.argv[1])
        self.db = None
        self.db_cursor = None
        self.date = date.today()
        self.create_db()

    def create_db(self):
        year = date.today().year
        month = date.today().month
        day = date.today().day
        name = '{year}_{month}_{day}.db'.format(year=year, month=month, day=day)
        self.db = sqlite3.connect(name)
        self.db_cursor = self.db.cursor()
        self.db_cursor.execute(SQL_CREATE_TABLE)
        self.db.commit()

    def serv(self):
        self.arduino.s.write(b'A')
        while True:
            results = {}
            for i in range(SENSORS_NUMBER):
                msg = self.arduino.recv_msg()
                sensor, val = msg.split(':', maxsplit=1)
                results[sensor] = float(val)

            if date.today().day != self.date.day:
                self.create_db()
            print(results)
            # Change it if db schema was changed
            self.db_cursor.execute(SQL_INSERT, (results['temperature1'], results['temperature2'], results['pressure']))
            self.db.commit()


if __name__ == '__main__':
    print('start serving...')
    DataServer().serv()
