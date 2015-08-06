#!/usr/bin/env python
#
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import MySQLdb

from flask import Flask
from flask import request, redirect, render_template, url_for
from flask import Response

app = Flask(__name__)

IP_ADDRESS = os.environ['CLOUDSQL_IP']
PASSWORD = os.environ['CLOUDSQL_PWD']
ZONE = os.environ['HOST_ZONE']

@app.route('/', methods=['GET', 'POST'])
def main_page():
    db = MySQLdb.connect(host=IP_ADDRESS, port=3306, db='guestbook', user='root', passwd=PASSWORD)
    cursor = db.cursor()
    if request.method == 'POST':
        cursor.execute('INSERT INTO entries (entry) VALUES (%s)', (request.form['entry'],))
        db.commit()
        db.close()
        return redirect(url_for('main_page'))
    else:
        cursor.execute('SELECT * FROM entries')
        entries = [row[1] for row in cursor.fetchall()]
        db.close()
        return render_template('main.html', entries=entries, zone=ZONE)

@app.route('/clear', methods=['POST'])
def clear_entries():
    db = MySQLdb.connect(host=IP_ADDRESS, port=3306, db='guestbook', user='root', passwd=PASSWORD)
    cursor = db.cursor()
    cursor.execute('DELETE from entries')
    db.commit()
    db.close()
    return redirect(url_for('main_page'))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
