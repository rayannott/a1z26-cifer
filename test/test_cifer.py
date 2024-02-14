import pytest

from cifer import A1Z26Cifer

@pytest.fixture()
def cifer_english():
    return A1Z26Cifer(language='en')

@pytest.fixture()
def cifer_russian():
    return A1Z26Cifer(language='ru')


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


def test_cifer_init_ru(cifer_russian: A1Z26Cifer):
    assert cifer_russian.language == 'ru'
    assert cifer_russian.letters == 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
    assert cifer_russian.DIGIT_MAP[1] == 'а' and cifer_russian.DIGIT_MAP[33] == 'я'
    assert cifer_russian.LETTER_MAP['а'] == '1' and cifer_russian.LETTER_MAP['я'] == '33'
    assert cifer_russian._failed_words == []
    assert next(cifer_russian._failed_cnt) == 0
    assert next(cifer_russian._failed_cnt) == 1


def test_cifer_encode_one(cifer_english: A1Z26Cifer):
    assert cifer_english._encode_one('a') == '1'
    assert cifer_english._encode_one('z') == '26'
    assert cifer_english._encode_one('aa') == '11'
    assert cifer_english._encode_one('k') == '11'


def test_cifer_encode_one_ru(cifer_russian: A1Z26Cifer):
    assert cifer_russian._encode_one('а') == '1'
    assert cifer_russian._encode_one('я') == '33'
    assert cifer_russian._encode_one('аа') == '11'
    assert cifer_russian._encode_one('й') == '11'


def test_cifer_encode(cifer_english: A1Z26Cifer):
    assert cifer_english.encode('abcd') == '1234'
    assert cifer_english.encode('a b c d') == '1 2 3 4'
    assert cifer_english.encode('a\t b; c d.') == '1 2 3 4'
    assert cifer_english.encode('hello') == '85121215'


def test_cifer_encode_ru(cifer_russian: A1Z26Cifer):
    assert cifer_russian.encode('абвг') == '1234'
    assert cifer_russian.encode('а б в г') == '1 2 3 4'
    assert cifer_russian.encode('а\t б; в г.') == '1 2 3 4'
    assert cifer_russian.encode('привет') == '1718103620'


@pytest.mark.skip('Not implemented')
def test_cifer_decode_one(cifer_english: A1Z26Cifer):
    ...


@pytest.mark.skip('Not implemented')
def test_cifer_decode(cifer_english: A1Z26Cifer):
    ...


@pytest.mark.skip('Not implemented')
def test_cifer_decode__one_ru(cifer_russian: A1Z26Cifer):
    ...


@pytest.mark.skip('Not implemented')
def test_cifer_decode_ru(cifer_russian: A1Z26Cifer):
    ...
