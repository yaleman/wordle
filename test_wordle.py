""" dumb tests """

import re

import pytest

from wordle import WordleThing, WORDFILE

# def test_wordle():
#     """ tests it works OK """
#     wordle = WordleThing(wordfile=WORDFILE)
#     tries = [
#         ("earth", "bbybb"),
#         ("wrong", "bgbbb"),
#         ("prism", "gggbb"),
#         ("prick", "ggggg"),
#     ]

#     for attempt, result in tries:
#         wordle.add_try(attempt, result)
#     assert True


def test_regex_gen_fullmatch():
    """ tests that a full match returns a full match """

    wordle = WordleThing(wordfile=WORDFILE)

    regex = wordle.generate_regex("saint", "ggggg")
    assert regex == re.compile("saint")


def test_regex_gen_allblack():
    """ tests that a full black result is fully banned """

    wordle = WordleThing(wordfile=WORDFILE)

    regex = wordle.generate_regex("saint", "bbbbb")
    expected_outcome = re.compile("[^ainst]{1}[^ainst]{1}[^ainst]{1}[^ainst]{1}[^ainst]{1}")
    assert regex == expected_outcome
