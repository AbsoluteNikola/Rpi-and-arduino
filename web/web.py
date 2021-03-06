"""
This is main file for web application
made with Flask
"""

import os
from time import sleep, time
from datetime import date
from random import choice, sample, random, randint
from subprocess import Popen
from flask import Flask, jsonify, request, make_response, abort
from RPi import GPIO
import sqlite3
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
    class for synchronization process when using pins and audio player
    """
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        while os.path.exists('{}.sync'.format(self.file_name)):
            sleep(0.01)
        open('{}.sync'.format(self.file_name), 'w').write('w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove('{}.sync'.format(self.file_name))


@app.route('/', methods=('GET',))
def index():
    """

    :return: index html on rout /
    """
    return app.send_static_file('index.html')


# @app.route('/playAudio', methods=['POST', 'GET'])
def play_audio(audio=''):
    if request.cookies.get('password') != COOKIE:
        abort(403)

    if not audio:
        audio = os.listdir('../data/audio/incoming')[-1]

    with Sync('audio') as sync:
        Popen(["ffplay", "-nodisp", "-autoexit", '../data/audio/incoming/{}'.format(audio)],
              stdout=open('/dev/null'),
              stderr=open('/dev/null'))
    return jsonify("ok")


@app.route('/getAudioList', methods=['GET'])
def get_audio_list():
    return jsonify(os.listdir('../data/audio/outgoing'))


@app.route('/getFilesList', methods=['GET'])
def get_files_list():
    return jsonify(os.listdir('../data/db') + os.listdir('../data/files/outgoing'))


@app.route('/putAudio', methods=['POST'])
def put_audio():
    if request.cookies.get('password') != COOKIE:
        abort(403)

    f = request.files['audio']
    f_name = str(time()).replace('.', '_')
    f.save("../data/audio/incoming/{}.wav".format(f_name))
    play_audio(f_name + '.wav')
    return jsonify('ok')


@app.route('/putFile', methods=['POST'])
def put_file():
    if request.cookies.get('password') != COOKIE:
        abort(403)

    f = request.files['file']
    f_name = request.form.get('name')
    f.save("../data/files/incoming/{}".format(f_name))
    return jsonify('ok')


@app.route('/checkLogin', methods=('POST', ))
def check_login():
    """
    check login, if it same with config's pass, set cookie for accept to pins control
    :return:
    """
    print(request.form.get('password'), PASSWORD)
    if request.form.get('password') == PASSWORD:
        resp = make_response('True')
        resp.set_cookie('password', COOKIE)
        return resp
    else:
        abort(403)


@app.route('/startDevice', methods=('POST', ))
def start_device():
    """
    run device like LED stripe and etc
    :return:
    """
    if request.cookies.get('password') != COOKIE:
        abort(403)

    with Sync('gpio') as sync:
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
    #    time_utc real,
    #    temperature_1 real,
    #    temperature_2 real,
    #    temperature_3 real,
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
    tm, t1, t2, t3, h, p_1, p_2, c2, c, v_s, v_h, g_x, g_y, g_z, a_x, a_y, a_z = res
    # cur.close()
    p = randint(1000, 1400)
    print(t1, t2, p)
    return jsonify({
        'temperature': [t1, t2, t3],
        'pressure': [p_1, p_2],
        'humidity': h,
        'CO2': c2,
        'fire': c > 3,
        'voltageSystem': v_s,
        'voltageHeater': v_h,
        'gyro': {
            'x': g_x,
            'y': g_y,
            'z': g_z
        },
        'accel': {
            'x': a_x,
            'y': a_y,
            'z': a_z
        }
    })
