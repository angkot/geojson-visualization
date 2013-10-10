from datetime import datetime
import json
import sqlite3

from bottle import get, post, run, request, static_file

db = sqlite3.connect('data.db')
cursor = db.cursor()

def init_db():
    # check table
    cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type=? AND name=?',
                   ('table', 'data'))
    cnt = cursor.fetchone()[0]
    if cnt == 0:
        # create table
        cursor.execute('CREATE TABLE data (id INTEGER PRIMARY KEY, ts TIMESTAMP, data BLOB)')

data = []

def load_db():
    global data

    cursor.execute('SELECT id, ts, data FROM data ORDER BY id')
    for row in cursor:
        data.append(dict(data_id=row[0],
                         timestamp=row[1],
                         data=json.loads(row[2])))

    print 'loaded {} data'.format(len(data))

@post('/store/<idx>')
def store(idx):
    idx = int(idx)
    if idx >= len(data):
        return dict(status='error', msg='invalid data index: {}'.format(idx))

    d = data[idx]
    cursor.execute('INSERT INTO data (ts, data) VALUES (?, ?)',
                   (datetime.strptime(d['timestamp'], '%Y-%m-%d %H:%M:%S'),
                    json.dumps(d['data'])))
    db.commit()

    d['data_id'] = cursor.lastrowid
    return dict(status='ok', data_id=d['data_id'])

@get('/get/<idx>')
def get_data(idx):
    idx = int(idx)
    if idx >= len(data):
        return dict(status='error', msg='invalid data index: {}'.format(idx))

    return dict(status='ok', data=data[idx])

@post('/save')
def save():
    p = request.forms.get('data')
    try:
        p = json.loads(p)
    except (ValueError, TypeError), e:
        print e
        return dict(status='error', msg='invalid data')

    data.append(dict(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     data_id=None, data=p))
    idx = len(data)

    return dict(status='ok', data_index=idx)

@get('/status')
def status():
    return dict(status='ok', total=len(data))

@get('/update')
def update():
    start = int(request.query.get('start', 0))
    return dict(status='ok', start=start,
                data=[dict(index=start+index,
                           timestamp=d['timestamp'],
                           id=d['data_id'])
                      for index, d in enumerate(data[start:])])

@get('/static/<fname>')
def static(fname):
    return static_file(fname, root='.')

@get('/')
def index():
    return static_file('index.html', root='.')

init_db()
load_db()
run(port=8000)

