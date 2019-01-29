from tasks.harvest import serialize_extractor_kwargs


def test_serialize_extractor_kwargs():
    args = ({'id': 1, 'name': 'foo'}, )
    kwargs = {'changed_name': {'key': 'name'}}

    r = serialize_extractor_kwargs(args, kwargs)

    assert r == {'changed_name': 'foo'}
