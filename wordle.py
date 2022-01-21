""" wordle handler """
# import click

from pathlib import Path
# import re
# import sys
from typing import Dict, List, Optional, Tuple

# import wordlist


WORDFILE = "/usr/share/dict/words"
filepath = Path(WORDFILE)

if not filepath.exists():
    raise ValueError("File doesn't exist.")

# print(len(wordle_list))


class WordleThing:
    """ my terrible handler for wordle """

    allowed_words: List[str] = []
    banned_letters: List[str] = []
    correct_letters: Dict[int, str] = {}
    misplaced_letters: List[str] = []
    lettercounts: Dict[str, Dict[int,int]] = {}
    wordscores: Dict[str, int] = {}

    tries: List[Tuple[str, str]] = []

    def __init__(
        self,
        wordlist: Optional[List[str]] = None,
        wordfile: Optional[str] = None
    ):
        """ startup """
        if wordlist:
            self.wordlist = wordlist
        if wordfile:
            self.load_wordlist(wordfile)

    def load_wordlist(self, filename: str):
        """ loads a list of words from a file """
        filetoload = Path(filename)
        if not filetoload.exists():
            raise FileNotFoundError(f"Couldn't find file: {filepath}")

        with filetoload.open(encoding="utf-8") as handle:
            self.wordlist = [word.strip().lower() for word in handle.readlines() if len(word.strip()) == 5]

    def calc_score(self, test_word: str) -> int:
        """generates a score based on the frequency of the letters in the word.
        The higher the score, the more likely it is to match the result.
        """
        wordscore = 0
        for i, letter in enumerate(test_word):
            if letter in self.lettercounts and i in self.lettercounts[letter]:
                wordscore += self.lettercounts[letter][i]
        return wordscore

    def process_tries(
        self,
        # tries: List[Tuple[str, str]],
    ) -> None:
        """ processes the user input """
        for attempt, res in self.tries:
            for i in range(5):
                attempt_letter = attempt[i].lower()
                result_letter = res[i].lower()
                if result_letter == "g":
                    self.correct_letters[i] = attempt_letter
                if result_letter == "b" and attempt_letter not in self.banned_letters:
                    self.banned_letters.append(attempt_letter)
                if result_letter == "y" and f"{i},{attempt_letter}" not in self.misplaced_letters:
                    self.misplaced_letters.append(f"{i},{attempt_letter}")

    def test_word(
        self,
        checkword: str,
    ) -> bool:
        """ tests if a given word is OK, returns a bool """
        for element in self.correct_letters: #pylint: disable=consider-using-dict-items
            if checkword[element] != self.correct_letters[element]:
                return False
        for banned_letter in self.banned_letters:
            if banned_letter in checkword:
                return False
        for mpl in self.misplaced_letters:
            ind, misplaced = mpl.split(",")
            if misplaced not in checkword and checkword[int(ind)] == mpl:
                return False
        return True

    def check_words(self):
        """ checks the wordlist """
        self.allowed_words = []

        for checkword in self.wordlist:
            if self.test_word(checkword):
                self.allowed_words.append(checkword)
                # build an index of lettercounts by their location in the word
                for i, letter in enumerate(checkword):
                    if letter not in self.lettercounts:
                        self.lettercounts[letter] = {}
                    if i not in self.lettercounts[letter]:
                        self.lettercounts[letter][i] = 0
                    self.lettercounts[letter][i] += 1


    def generate_wordscores(self):
        """ generates wordscores """
        self.wordscores = {}

        for allowed_word in wordle.allowed_words:
            self.wordscores[allowed_word] = self.calc_score(allowed_word)

    @classmethod
    def validate_result_entry(cls, result_input: str) -> str:
        """ validates an entered result"""
        result_input = result_input.lower().strip()
        if len(result_input) != 5:
            raise ValueError(f"Invalid input length, should be 5, got {len(result_input)}")
        for letter in result_input:
            if letter not in ["b", "g", "y"]:
                raise ValueError(f"Invalid letters in entry, need to be one of bgy, got: {result_input}")
        return result_input

    def validate_attempt_entry(self, attempt: str) -> str:
        """ validates an entered attempt"""
        attempt = attempt.lower().strip()
        if len(attempt) != 5:
            raise ValueError(f"Invalid input length, should be 5, got {len(attempt)}")
        if attempt not in self.wordlist:
            raise ValueError(f"Invalid attempt word: {attempt} not in wordlist.")
        return attempt

    def add_try(self, attempted_word: str, result_input: str):
        """ takes an attempt and the result, adds it to the list """
        # if len(attempted_word) != 5 or len(result) != 5:
            # raise ValueError("Invalid length of one of the input vals")
                # raise ValueError("Invalid result value)")

        self.tries.append((
            self.validate_attempt_entry(attempted_word),
            self.validate_result_entry(result_input)))


        self.process_tries()
        self.check_words()
        self.generate_wordscores()


    def list_tries(self):
        """ lists the attempts """
        for attempt, attempt_result in self.tries:
            print(f"{attempt}\t{attempt_result}")

    def print_results(self) -> bool:
        """ display the things """

        print(f"Banned: {''.join(self.banned_letters)}")
        print(f"Misplaced: {' '.join(self.misplaced_letters)}")
        print(f"Correct: {self.correct_letters}")

        if len(self.wordscores.keys()) == 1:
            firstword = [ word for word in self.wordscores][-1]
            print(f"Found word: {firstword}")
            return True
        else:
            scoredlist = sorted((value, key) for (key, value) in self.wordscores.items())
            for score, word in reversed(scoredlist[-5:]):
                print(f"{score} - {word}")
        return False

wordle = WordleThing(wordfile=WORDFILE)


# while True:
#     attempt_word = input("Word you tried: ").strip()
#     result = input("Result (list of gbyy): ").strip()
#     try:
#         wordle.add_try(attempt_word, result)
#     except ValueError as input_error:
#         print(f"Input validation error: {input_error}")
#     wordle.process_tries()
#     wordle.check_words()
#     wordle.generate_wordscores()
#     wordle.print_results()

