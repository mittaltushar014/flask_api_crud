import csv
from datetime import date, timedelta
from io import StringIO
import requests
from app import app, celery
from datetime import datetime
import traceback


def format_covid_data(csv_data):
    csv_dicts = []
    for row in csv_data:
        data = dict(row)
        for field in ['Confirmed', 'Deaths', 'Recovered', 'Active']:
            data[field] = int(data[field])
        data['Location'] = f"{data['Lat']}, {data['Long_']}"
        del data['Lat']
        del data['Long_']
        csv_dicts.append(data)
    return csv_dicts


def save_error_log(log_file, exception):
    '''Save a traceback to a file, in case of an unexpected error.'''
    error_log = open(log_file, 'a')
    time_now = datetime.utcnow()
    error = f'Error\nTime: {time_now.strftime("%Y/%m/%d, %H:%M:%S")} UTC\n'\
        + f'\n{exception}\n{traceback.format_exc()}\n'
    error_log.write(error)
    error_log.close()


@celery.task(name="tasks.update_covid_stats")
def update_covid_stats(index):
    '''Downloads COVID-19 infection stats from a URL and adds it to an
    elastic search index.'''

    print("Getting data from server...\n")
    for days in range(0, 10):
        data_date = (date.today() - timedelta(days=days)).strftime("%m-%d-%Y")
        url = app.config['COVID_DATA_URL'].format(data_date)
        response = requests.get(url)
        if response.status_code == 200:
            break
    csv_data = StringIO(response.text)
    print("Done.\n")

    print("Formatting data...\n")
    csv_dicts = format_covid_data(csv.DictReader(csv_data, delimiter=","))

    print("Done.\nUpdating elasticsearch index data...\n")
    if app.elasticsearch.indices.exists(index):
        app.elasticsearch.indices.delete(index=index)

    app.elasticsearch.indices.create(index=index,
                                     body=app.config['COVID_DATA_MAPPING'])
    try:
        for row_dict in csv_dicts:
            app.elasticsearch.index(index=index, body=row_dict)
    except Exception as exception:
        save_error_log(LOG_FILE, exception)

    print("Done.\n")
