import importlib


def get_callable(module_path):
    (module_name, callable_name) = module_path.rsplit('.', 1)

    module = importlib.import_module(module_name)
    _callable = getattr(module, callable_name)

    return _callable


def call_callable(module_path, configuration):
    return get_callable(module_path)(**configuration)
