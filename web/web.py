import sqlite3
from flask import Flask, jsonify
from random import choice
import os
app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/getInfo', methods=['GET', ])
def get_info():
    name = os.listdir('../data')[-1]
    cur = sqlite3.connect('../data/{}'.format(name)).cursor()
    # cur.execute("""SELECT * FROM sensors WHERE "rowid" = (SELECT max("rowid") FROM sensors)""")
    cur.execute("""SELECT * FROM sensors;""")
    t1, t2, p = choice(cur.fetchall())
    cur.close()
    print(t1, t2, p)
    return jsonify({
        'temperature': [t1, t2, ],
        'pressure': p
    })
