from celery import current_app
from celery import states

from celery import Task


def serialize_extractor_kwargs(args, kwargs):
    """Returns extractor kwargs dict

    Params
        args: tuple which has item type is dict.
        kwargs: dict object which key is item's key in args,
                each value has 'key', 'value' for references of args item.

    Example
        >>> args = ({'id': 1, 'name': 'foo'}, )
        >>> kwargs = {'changed_name': {'key': 'name'}}
        >>> r = serialize_extractor_kwargs(args, kwargs)
        >>> r == {'changed_name': 'foo'}
    """

    if len(args) == 0:
            args = ({},)

    resolved_extractor_kwargs = {}
    for k, v in kwargs.items():
        value = v.get('value', args[0].get(v.get('key')))
        resolved_extractor_kwargs[k] = value

    return resolved_extractor_kwargs


class Harvest(Task):
    name = 'harvest'

    def run(self, *args, harvester, harvester_type, **kwargs):
        harvester = current_app.extractors[harvester][harvester_type]

        try:
            extractor_kwargs = serialize_extractor_kwargs(args, kwargs)
            news_content = harvester.extract(**extractor_kwargs)

            return news_content

        except Exception as exc:
            # Celery Issues: 4222
            self.update_state(state=states.FAILURE)
            return {'exc': str(exc)}
