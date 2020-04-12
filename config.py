'''For the configurations rquired in the project'''

import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SEARCH_INDEX = 'data_covid'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:tushar-123@corona-flask-db.ckgbqi9rzpou.us-east-2.rds.amazonaws.com:5432/postgres"    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = "vpc-corona-flask-es-jd6nq2w2lvkt4h7yloixdeh2au.us-east-2.es.amazonaws.com:80"
    
    SEARCH_INDEX = 'forum_data'

    HOSTNAME = 'http://127.0.0.1:5000'

    COVID_DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/" +\
        "COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" +\
        "{}.csv"

    COVID_DATA_INDEX = 'covid_stats'

    COVID_DATA_MAPPING = {
        "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "FIPS": {
                    "type": "integer"
                },
                "Admin2": {
                    "type": "text"
                },
                "Province_State": {
                    "type": "text"
                },
                "Country_Region": {
                    "type": "text"
                },
                "Last_Update": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "Location": {
                    "type": "geo_point",
                    "ignore_malformed": True
                },
                "Confirmed": {
                    "type": "long"
                },
                "Deaths": {
                    "type": "long"
                },
                "Recovered": {
                    "type": "long"
                },
                "Active": {
                    "type": "long"
                },
                "Combined_Key": {
                    "type": "text"
                }
            }
        }
    }


CELERY_CONFIG = {
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0',
    'task_track_started': True,
    'beat_schedule': {
        "five-minute-task": {
            "task": "tasks.refresh_index",
            "schedule": crontab(minute='*/5'),
            "args": ['forum_data']
        }
    }
}
