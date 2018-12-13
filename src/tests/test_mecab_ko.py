import mecab

m = mecab.MeCab()


def test_mecab_should_be_working():
    text = '안녕하세요.'
    parsed = m.pos(text)

    assert type(parsed) is list
