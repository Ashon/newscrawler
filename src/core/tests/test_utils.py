from core.utils import get_callable
from core.utils import call_callable


def simple_fn():
    return 1


def test_get_callable_should_returns_callable():
    fn = get_callable('core.tests.test_utils.simple_fn')
    assert callable(fn)


def test_call_callable_should_returns_functions_result():
    result = call_callable('core.tests.test_utils.simple_fn', {})
    assert result == 1
