import sqlite3
import os
from time import sleep
from flask import Flask, jsonify, request, make_response, abort
from RPi import GPIO
from set_up_pi import set_up
from random import choice, sample
from secrets import PASSWORD, COOKIE

app = Flask(__name__)

LIGHT = 5
AIR = 3


class Sync:
    def __enter__(self):
        while os.path.exists('sync'):
            sleep(0.01)
        open('sync', 'w').write('w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove('sync')


with Sync:
    set_up()


@app.route('/', methods=('GET',))
def index():
    return app.send_static_file('index.html')


@app.route('/checkLogin', methods=('POST', ))
def check_login():
    print(request.form.get('password'))
    if request.form.get('password') == PASSWORD:
        resp = make_response('True')
        resp.set_cookie('password', COOKIE)
    else:
        resp = make_response('False')
    return resp


@app.route('/getAdmin', methods=('GET', ))
def get_admin():

    return app.send_static_file('admin.html')


@app.route('/startDevice', methods=('POST', ))
def start_device():
    if request.cookies.get('password') != COOKIE:
        return "you are not authorized"
    with Sync:
        GPIO.setmode(GPIO.BOARD)


@app.route('/getInfo', methods=('GET',))
def get_info():
    name = os.listdir('../data/db')[-1]
    print(name)
    cur = sqlite3.connect('../data/db/{}'.format(name)).cursor()
    cur.execute("""SELECT * FROM sensors WHERE "rowid" = (SELECT max("rowid") FROM sensors)""")
    # cur.execute("""SELECT * FROM sensors;""")
    # temperature_1 real,
    # temperature_2 real,
    # temperature_3 real,
    #
    # humidity real,
    # pressure real,
    # CO2 real,
    # CO real?
    t1, t2, h, p, c, _ = cur.fetchone()
    cur.close()
    print(t1, t2, p)
    return jsonify({
        'temperature': [t1, t2],
        'pressure': p,
        'humidity': h,
        'CO2': c
    })
