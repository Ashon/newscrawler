from celery import Celery

from core.utils import get_callable


def load_extractors(extractor_config):
    extractors = {}
    for extractor_name, callable_conf in extractor_config.items():
        _callable = get_callable(callable_conf['callable'])
        link_extractor, content_extractor = _callable()

        extractors[extractor_name] = {
            'link': link_extractor,
            'content': content_extractor
        }

    return extractors


def initialize_applictaion(settings):
    app = Celery(__name__)
    app.config_from_object(settings)

    extractors = load_extractors(settings.EXTRACTOR_CONFIG)
    setattr(app, 'extractors', extractors)

    return app
