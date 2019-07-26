"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import openaq

API = openaq.OpenAQ()
STATUS, BODY = API.measurements(city='Los Angeles', parameter='pm25')

APP = Flask(__name__)
APP.config['SQLACHEMY_DATABSE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    """Base view."""

def get_data():
    data = []
    for i in list(range(len(BODY['results']))):
        data.append((BODY['results'][i]['date']['utc'], BODY['results'][i]['value']))
        return data
    
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Record {}, \n Datetime:{}, \n Value:{}> \n\n'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    results = get_data()
    id = 0
    
    for i in list(range(len(results))):
        id = id + 1
        data = Record(id=id,
                      datetime=results[i][0],
                      value=results[i][1])
        DB.session.add(data)
    DB.session.commit()
    return redirect(url_for('root'))
     #'Data refreshed!'
