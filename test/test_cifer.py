import pytest

from cifer import A1Z26Cifer


def test_cifer_init():
    c = A1Z26Cifer(language='en')
    assert c.language == 'en'
    assert c.letters == 'abcdefghijklmnopqrstuvwxyz'
    assert c.DIGIT_MAP[1] == 'a' and c.DIGIT_MAP[26] == 'z'
    assert c.LETTER_MAP['a'] == '1' and c.LETTER_MAP['z'] == '26'
    assert c._failed_words == []
    assert next(c._failed_cnt) == 0
    assert next(c._failed_cnt) == 1

def test_cifer_encode_one():
    c = A1Z26Cifer(language='en')
    assert c._encode_one('a') == '1'
    assert c._encode_one('z') == '26'
    assert c._encode_one('aa') == '11'
    assert c._encode_one('k') == '11'

def test_cifer_encode():
    c = A1Z26Cifer(language='en')
    assert c.encode('abcd') == '1234'
    assert c.encode('a b c d') == '1 2 3 4'
    assert c.encode('a\t b; c d.') == '1 2 3 4'
    assert c.encode('hello') == '85121215'

def test_cifer_decode_one():
    ...

def test_cifer_decode():
    ...
