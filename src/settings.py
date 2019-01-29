import os

env = os.environ


BROKER_URL = env.get('BROKER_URL')
CELERY_RESULT_BACKEND = env.get('BACKEND_URL')

EXTRACTOR_CONFIG = {
    'naver': {
        'callable': 'extractors.naver.load_extractor'
    }
}

CELERY_TRACK_STARTED = True
CELERY_ROUTES = {
    'distribute_chain': {'queue': 'distribute_chain'},
    'harvest': {'queue': 'harvest'},
    'extract': {'queue': 'extract'},
    'aggregate': {'queue': 'aggregate'}
}
