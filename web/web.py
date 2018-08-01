import sqlite3
import os
from flask import Flask, jsonify, request, make_response, abort
from random import choice
from secrets import PASSWORD, COOKIE
app = Flask(__name__)


@app.route('/', methods=('GET',))
def index():
    return app.send_static_file('index.html')


@app.route('/checkLogin', methods=('POST',))
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
    if request.cookies.get('password') != COOKIE:
        return abort(401)

    return app.send_static_file('admin.html')


@app.route('/getInfo', methods=('GET',))
def get_info():
    name = os.listdir('../data/db')[-1]
    print(name)
    cur = sqlite3.connect('../data/db/{}'.format(name)).cursor()
    # cur.execute("""SELECT * FROM sensors WHERE "rowid" = (SELECT max("rowid") FROM sensors)""")
    cur.execute("""SELECT * FROM sensors;""")
    t1, t2, p = choice(cur.fetchall())
    cur.close()
    print(t1, t2, p)
    return jsonify({
        'temperature': [t1, t2, ],
        'pressure': p
    })
