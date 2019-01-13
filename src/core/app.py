from celery import Celery


def initialize_applictaion(settings):
    app = Celery(__name__, broker=settings.BROKER_URL, backend=settings.BACKEND_URL)
    app.conf.task_routes = settings.TASK_ROUTES
    app.conf.task_track_started = True

    return app
