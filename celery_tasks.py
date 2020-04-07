'''Background Celery tasks'''

from app import es, celery
from io import StringIO
from datetime import timedelta, date
import requests
import csv


@celery.task
def update_es():
    print('Doing database update')
    if es.ping():
        print('Database connection done')
        print('Existing data check')
        if es.indices.exists('covid_cases'):
            remove_data()
            dump_data()
        else:
            print('No older data found')
            dump_data()
    else:
        print('Connection with Database failed')


def remove_data():
    print('Removing old data')
    es.indices.delete('covid_cases')
    print('Deleted')


def dump_data():
    print('Fetching data')
    es.indices.create('covid_cases')
    today = date.today() - timedelta(days=1)
    today = today.strftime("%m-%d-%Y")
    response_text = requests.get(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" +
        today +
        ".csv").text
    csv_data = StringIO(response_text)
    csv_dict = csv.DictReader(csv_data)
    id = 0
    for data in csv_dict:
        id += 1
        es.index(index='covid_cases', body=data, id=id)
    print(f'Loaded {id} records')
