import sqlite3
from datetime import date
from flask import Flask

app = Flask(__name__)


@app.route('/')
def result():
    year = date.today().year
    month = date.today().month
    day = date.today().day
    name = '{year}_{month}_{day}.db'.format(year=year, month=month, day=day)
    cur = sqlite3.connect('../data/{}'.format(name)).cursor()
    cur.execute("""SELECT * FROM sensors ORDER BY "id" DESC LIMIT 1;""")
    t1, t2, p = cur.fetchone()
    cur.close()
    return "temperature1 = {}\ntemperature2 = {}\npressure = {}".format(t1, t2, p)
