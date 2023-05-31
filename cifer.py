from itertools import count, product
from string import ascii_lowercase

import enchant

# encode tools
class Encoder:
    LETTER_MAP = {ch: str(i) for i, ch in enumerate(ascii_lowercase, 1)}

    def _clean_sentence(self, sentence: str) -> str:
        res = ''
        for ch in sentence:
            if ch.isspace():
                res += ' '
            elif ch.isalpha():
                res += ch.lower()
        return res

    def _encode_one(self, s: str) -> str:
        '''Encodes one word'''
        return ''.join(map(self.LETTER_MAP.get, s))
    
    def encode(self, sentence: str):
        '''Cleans (removes non-alpha characters) and encodes the whole sentence.'''
        return ' '.join(
            self._encode_one(w) 
            for w in self._clean_sentence(sentence).split()
        )

# decode tools
class Decoder:
    ENG_UK = enchant.Dict('en_UK')
    ENG_US = enchant.Dict('en_US')
    DIGIT_MAP = {i: ch for i, ch in enumerate(ascii_lowercase, 1)}

    def __init__(self) -> None:
        self._reset()

    def _reset(self):
        self._failed_words = []
        self._failed_cnt = count()

    @staticmethod
    def _split_into_letterable(digits: str) -> list[str]:
        '''
        Splits a digit-string into a list of letterable digit-strings.
        Ex.: '1293' -> ['12', '9', '3']
        '''
        if len(digits) == 1:
            return [digits]
        to_ret = []
        s = ''
        for i in range(len(digits)-1):
            s += digits[i]
            if int(digits[i:i+2]) > 26:
                to_ret.append(s)
                s = ''
        s += digits[-1]
        to_ret.append(s)
        return to_ret

    def _get_all_combinations(self, digits: str) -> list[list[int]]:
        '''
        Core algorithm that returns a list of all allowed
        partitions of a letterable digit-string.
        Ex.: '15' -> [['1', '5'], ['15']]
        '''
        if digits.startswith('0'):
            return []
        if len(digits) == 0:
            return [[]]
        if len(digits) == 1:
            return [[int(digits)]]
        to_ret = []
        for i in [1, 2]:
            one_or_two_digits = int(digits[:i])
            rest = self._get_all_combinations(digits[i:])
            for lst in rest:
                to_ret.append([one_or_two_digits] + lst)
        return to_ret

    def _transform_combinations_to_words(self, digits: list[list[int]]) -> list[str]:
        '''
        digits -- letterable digit-string
        Ex.: '15' -> ['ae', 'o'] (because '1','5' is 'ae'; '15' is 'o')
        '''
        return [
            ''.join(map(self.DIGIT_MAP.get, combination))
                for combination in self._get_all_combinations(digits)
        ]

    def _all_possible_decodings(self, encoded_word: str) -> list[str]:
        '''
        Returns the product of all possible options for every word part.
        Applies _transform_combinations_to_words right away.
        Ex.: '1511' -> ['aeaa', 'aek', 'oaa', 'ok']
        '''
        to_ret = []
        letterables = self._split_into_letterable(encoded_word)
        all_word_combinations = [
            self._transform_combinations_to_words(letterable) 
                for letterable in letterables
        ]
        return [''.join(word_parts) for word_parts in product(*all_word_combinations)]

    def _decode_one(self, encoded_word: str) -> list[str]:
        '''
        Decodes one word. 
        Returns all decodings which can be found in the corpus (namely, existing words).
        Caches failed words.
        '''
        ap = self._all_possible_decodings(encoded_word)
        to_ret = [
                word 
                for word in ap
                if self.ENG_UK.check(word) or self.ENG_US.check(word)
            ]
        if not to_ret:
            self._failed_words.append(sorted(ap, key=len))
        return to_ret
    
    def decode(self, encoded_sentence: str) -> str:
        '''Decodes one sentence.
        Returns a string with all options for
        one word separated by "pipe"(|) symbol.
        Places '<ID>?' in place of failed words. Possible decodings for
        those words can be looked at using get_failed_words_dict()[ID]
        '''
        self._reset()
        def resolve(word):
            options = self._decode_one(word)
            if options:
                return '|'.join(options)
            else:
                failed_index = next(self._failed_cnt)
                return f'[{self._failed_words[failed_index][0]}]{failed_index}?'
        return ' '.join(
            resolve(word) for word in encoded_sentence.split()
        )
    
    def get_failed_words_dict(self) -> dict[int, list[str]]:
        return {i: '|'.join(words) for i, words in enumerate(self._failed_words)}
