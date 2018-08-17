import sqlite3
import os
from time import sleep
from flask import Flask, jsonify, request, make_response, abort
from RPi import GPIO
from random import choice, sample
from secrets import PASSWORD, COOKIE

app = Flask(__name__)

pins = {
    'CO2plus': 7,
    'CO2minus': 3,
    'Light': 5,
    'Heater': 8
}


class Sync:
    def __enter__(self):
        while os.path.exists('sync.txt'):
            sleep(0.01)
        open('sync.txt', 'w').write('w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove('sync.txt')


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
        return jsonify('Error')
    with Sync() as sync:
        GPIO.setmode(GPIO.BOARD)
        sensor = pins.get(request.form.get('sensor'))
        GPIO.setup(sensor, GPIO.OUT)
        if sensor == 'CO2plus ':

            p = GPIO.PWM(7, 50)
            p.start(0)
            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                sleep(0.1)
            return jsonify(True)
        if not sensor:
            return jsonify('Error')
        GPIO.output(sensor, GPIO.input(sensor) ^ 1)
    return jsonify(GPIO.input(sensor) == GPIO.HIGH)


@app.route('/getInfo', methods=('GET',))
def get_info():
    name = os.listdir('../data/db')[-1]
    print(name)
    cur = sqlite3.connect('../data/db/{}'.format(name)).cursor()
    # cur.execute("""SELECT * FROM sensors WHERE "rowid" = (SELECT max("rowid") FROM sensors)""")
    cur.execute("""SELECT temperature_1, temperature_2, humidity, pressure, CO2, CO FROM sensors WHERE "rowid" = (SELECT max("rowid") FROM sensors);""")
    # temperature_1 real,
    # temperature_2 real,
    #
    # humidity real,
    # pressure real,
    # CO2 real,
    # CO real?
    res = cur.fetchone()
    print(res)
    t1, t2, h, p, c2, c = res[0:]
    cur.close()
    print(t1, t2, p)
    return jsonify({
        'temperature': [t1, t2],
        'pressure': p,
        'humidity': h,
        'CO2': c2,
        'fire': False if c < 50 else True
    })
