import pytest

from cifer import A1Z26Cifer

@pytest.fixture()
def cifer_english():
    return A1Z26Cifer(language='en')


def test_cifer_init_default():
    cifer = A1Z26Cifer()
    assert cifer.language == 'en'


def test_cifer_init_other():
    with pytest.raises(ValueError):
        A1Z26Cifer(language='other')


def test_cifer_init(cifer_english: A1Z26Cifer):
    assert cifer_english.language == 'en'
    assert cifer_english.letters == 'abcdefghijklmnopqrstuvwxyz'
    assert cifer_english.DIGIT_MAP[1] == 'a' and cifer_english.DIGIT_MAP[26] == 'z'
    assert cifer_english.LETTER_MAP['a'] == '1' and cifer_english.LETTER_MAP['z'] == '26'
    assert cifer_english._failed_words == []
    assert next(cifer_english._failed_cnt) == 0
    assert next(cifer_english._failed_cnt) == 1


def test_cifer_encode_one(cifer_english: A1Z26Cifer):
    assert cifer_english._encode_one('a') == '1'
    assert cifer_english._encode_one('z') == '26'
    assert cifer_english._encode_one('aa') == '11'
    assert cifer_english._encode_one('k') == '11'


def test_cifer_encode(cifer_english: A1Z26Cifer):
    assert cifer_english.encode('abcd') == '1234'
    assert cifer_english.encode('a b c d') == '1 2 3 4'
    assert cifer_english.encode('a\t b; c d.') == '1 2 3 4'
    assert cifer_english.encode('hello') == '85121215'


def test_cifer_decode_one(cifer_english: A1Z26Cifer):
    ...


def test_cifer_decode(cifer_english: A1Z26Cifer):
    ...
