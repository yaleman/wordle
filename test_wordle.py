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

@pytest.fixture(name="wordle")
def fixture_wordle():
    """ factory """
    return  WordleThing(wordfile=WORDFILE)

def test_regex_gen_fullmatch(wordle):
    """ tests that a full match returns a full match """

    regex = wordle.generate_regex("saint", "ggggg")
    assert regex == re.compile("saint")


def test_regex_gen_allblack(wordle):
    """ tests that a full black result is fully banned """
    regex = wordle.generate_regex("saint", "bbbbb")
    expected_outcome = re.compile("[^ainst]{1}[^ainst]{1}[^ainst]{1}[^ainst]{1}[^ainst]{1}")
    assert regex == expected_outcome


def test_regex_gen_complex(wordle):
    """ tests a complicated one """

    regex = wordle.generate_regex("genie", "bbgyg")
    expected_outcome = re.compile(r"[^eg]{1}[^eg]{1}n[^egi]{1}e")
    assert regex == expected_outcome

def test_regex_gen_complex2(wordle):
    """ tests another complicated one """

    regex = wordle.generate_regex("pinny", "bggbb")
    expected_outcome = re.compile(r"[^npy]{1}in[^npy]{1}[^npy]{1}")
    assert regex == expected_outcome
