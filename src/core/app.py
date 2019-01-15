from celery import Celery

from core.utils import get_callable


def initialize_applictaion(settings):
    app = Celery(__name__, broker=settings.BROKER_URL, backend=settings.BACKEND_URL)
    app.conf.task_routes = settings.TASK_ROUTES
    app.conf.task_track_started = True

    extractors = {}
    for extractor_name, callable_conf in settings.EXTRACTOR_CONFIG.items():
        _callable = get_callable(callable_conf['callable'])
        link_extractor, content_extractor = _callable()

        extractors[extractor_name] = {
            'link': link_extractor,
            'content': content_extractor
        }

    setattr(app, 'extractors', extractors)

    return app
