import string

from src.handy import ispunctuation


class TestHandy:
    def test_ispunctuation(self):
        assert not ispunctuation('')

        for c in string.printable:
            if c in string.punctuation:
                assert ispunctuation(c)
            else:
                assert not ispunctuation(c)
