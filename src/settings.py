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
    'core.workflows.distribute_chain': {'queue': 'distribute_chain'},
    'worker.harvest_links': {'queue': 'harvest_links'},
    'worker.harvest_content': {'queue': 'harvest_content'},
    'worker.extract': {'queue': 'extract'},
    'worker.aggregate_words': {'queue': 'aggregate_words'}
}
