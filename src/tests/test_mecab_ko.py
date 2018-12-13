import mecab

m = mecab.MeCab()


def test_mecab_should_be_working():
    text = '안녕하세요.'

    parsed_pos = m.pos(text)
    parsed_nouns = m.nouns(text)
    parsed_morphs = m.morphs(text)

    assert type(parsed_pos) is list
    assert type(parsed_nouns) is list
    assert type(parsed_morphs) is list
