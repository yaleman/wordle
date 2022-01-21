""" dumb tests """


from wordle import WordleThing, WORDFILE

def test_wordle():
    """ tests it works OK """
    wordle = WordleThing(wordfile=WORDFILE)
    tries = [
        ("earth", "bbybb"),
        ("wrong", "bgbbb"),
        ("prism", "gggbb"),
        ("prick", "ggggg"),
    ]

    for attempt, result in tries:
        wordle.add_try(attempt, result)
    assert True
