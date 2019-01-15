import os

env = os.environ


BROKER_URL = env.get('BROKER_URL')
BACKEND_URL = env.get('BACKEND_URL')

EXTRACTOR_CONFIG = {
    'naver': {
        'callable': 'extractors.naver.load_extractor'
    }
}

TASK_ROUTES = {
    'core.workflows.distribute_chain': {'queue': 'distribute_chain'},
    'worker.harvest_links': {'queue': 'harvest_links'},
    'worker.harvest_content': {'queue': 'harvest_content'},
    'worker.extract_nouns': {'queue': 'extract_nouns'},
    'worker.aggregate_words': {'queue': 'aggregate_words'}
}
