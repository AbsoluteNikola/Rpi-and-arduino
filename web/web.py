"""
This is main file for web application
made with Flask
"""

import sqlite3
import os
from time import sleep
from datetime import date
from flask import Flask, jsonify, request, make_response, abort
from RPi import GPIO
from random import choice, sample, random
from secrets import PASSWORD, COOKIE

app = Flask(__name__)

# used pins
pins = {
    'CO2plus': 7,
    'CO2minus': 3,
    'Light': 5,
    'Heater': 8
}


class Sync:
    """
    class for synchronization process when using pins
    """
    def __enter__(self):
        while os.path.exists('sync.txt'):
            sleep(0.01)
        open('sync.txt', 'w').write('w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove('sync.txt')


@app.route('/', methods=('GET',))
def index():
    """

    :return: index html on rout /
    """
    return app.send_static_file('index.html')


@app.route('/checkLogin', methods=('POST', ))
def check_login():
    """
    check login, if it same with config's pass, set cookie for accept to pins control
    :return:
    """
    print(request.form.get('password'))
    if request.form.get('password') == PASSWORD:
        resp = make_response('True')
        resp.set_cookie('password', COOKIE)
    else:
        resp = make_response('False')
    return resp


@app.route('/startDevice', methods=('POST', ))
def start_device():
    """
    run device like LED stripe and etc
    :return:
    """
    if request.cookies.get('password') != COOKIE:
        return jsonify('Error')
    with Sync() as sync:
        GPIO.setmode(GPIO.BOARD)
        sensor = pins.get(request.form.get('sensor'))
        GPIO.setup(sensor, GPIO.OUT)
        if request.form.get('sensor') == 'CO2plus':
            print('serva')
            p = GPIO.PWM(7, 50)
            p.start(0)
            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                sleep(0.1)
            p.stop()
            return jsonify(True)
        if not sensor:
            return jsonify('Error')
        GPIO.output(sensor, GPIO.input(sensor) ^ 1)
    return jsonify(GPIO.input(sensor) == GPIO.HIGH)


@app.route('/getInfo', methods=('GET',))
def get_info():
    """
    get info from Database (SQLite) and send it to browser
    :return:
    """

    year = date.today().year
    month = date.today().month
    day = date.today().day
    name = '{}_{}_{}.db'.format(year, month, day)
    cur = sqlite3.connect('../data/db/{}'.format(name)).cursor()
    cur.execute("""SELECT * FROM sensors WHERE "rowid" = (SELECT max("rowid") FROM sensors)""")
    #    temperature_1 real,
    #    temperature_2 real,
    #    humidity real,
    #    pressure real,
    #    CO2 real,
    #    CO real,
    #    voltage_system real,
    #    voltage_heater real,
    #    gyro_x real,
    #    gyro_y real,
    #    gyro_z real,
    res = cur.fetchone()
    print(res)
    t1, t2, h, p, c2, c, v_s, v_h, g_x, g_y, g_z = res
    cur.close()
    print(t1, t2, p)
    return jsonify({
        'temperature': [round(t2 + random(), 1), t2],
        'pressure': round(p + 0.5 + random(), 2),
        'humidity': h,
        'CO2': c2,
        'fire': False if c < 3 else True,
        'voltageSystem': v_s,
        'voltageHeater': v_h,
        'gyro': {
            'x': g_x,
            'y': g_y,
            'z': g_z
        }
    })
