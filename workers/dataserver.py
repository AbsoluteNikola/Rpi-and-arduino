import sys
import os
import sqlite3
from datetime import date
from arduino import ArduinoConn, SENSORS_NUMBER

SQL_CREATE_TABLE = """
    CREATE TABLE sensors (
        temperature_1 real,
        temperature_2 real,
        temperature_3 real,
        humidity real,
        pressure real,
        CO2 real,
        CO real
    );
"""

SQL_INSERT = """
    INSERT INTO sensors VALUES (:temperature_1, :temperature_2, :temperature_3, :humidity, :pressure, :CO2, :CO);
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
        name = '../data/db/{year}_{month}_{day}.db'.format(year=year, month=month, day=day)
        self.db = sqlite3.connect(name)
        self.db_cursor = self.db.cursor()
        try:
            self.db_cursor.execute(SQL_CREATE_TABLE)
            self.db.commit()
        except sqlite3.OperationalError:
            pass

    def serve(self):
        self.arduino.s.write(b'A')
        while True:
            results = {}
            for i in range(SENSORS_NUMBER):
                msg = self.arduino.recv_msg()
                print(msg)
                sensor, val = msg.split(':', maxsplit=1)
                results[sensor] = float(val)

            if date.today().day != self.date.day:
                self.create_db()
                self.date = date.today()
            print(results)

            self.db_cursor.execute(SQL_INSERT, results)
            self.db.commit()


if __name__ == '__main__':
    print('start serving...')
    DataServer().serve()
