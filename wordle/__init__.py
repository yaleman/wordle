""" wordle handler """
# import click

from pathlib import Path
import re
import sys
from typing import Dict, List, Optional, Tuple

# from .wordlist import wordle_list, second_wordle_list

WORDFILE = "/usr/share/dict/words"

class WordleThing:
    """ my terrible handler for wordle """

    allowed_words: List[str] = []
    banned_letters: List[str] = []
    correct_letters: Dict[int, str] = {}
    misplaced_letters: List[str] = []
    lettercounts: Dict[str, Dict[int,int]] = {}
    wordscores: Dict[str, int] = {}

    tries: List[Tuple[str, str]] = []

    regexes: List[Tuple[str, re.Pattern]] = []

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
            raise FileNotFoundError(f"Couldn't find file: {filetoload.as_posix()}")

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

    def generate_regex(self, attempt, outcome) -> Tuple[str, re.Pattern]:
        """ generates a regex based on the attempt and result"""
        # self.regexes = []

        notintheword = ""
        required_letters = ""
        # first, iterate over the word to find the "not in this word" letters
        if "b" in outcome:
            for index, letter in enumerate(attempt):
                if outcome[index] == "b":
                    print(f"adding {letter}")
                    notintheword = ''.join(sorted(set(f"{notintheword}{letter}")))
        if "y" in outcome:
            for index, letter in enumerate(attempt):
                if outcome[index] == "y":
                    print(f"adding {letter}")
                    required_letters = ''.join(sorted(set(f"{required_letters}{letter}")))
        print(f"Required letters: {required_letters}")
        print(f"Banned letters: {notintheword}")

        # add the things
        regex_result = r"^"
        for i in range(5):
            attempt_letter = attempt[i].lower()
            result_letter = outcome[i].lower()
            if result_letter == "g":
                self.correct_letters[i] = attempt_letter
                regex_result = regex_result + attempt_letter# + r"{1}"
                print(f"g - {regex_result}")
            if result_letter == "b":
                letterstodrop = ''.join(sorted(set(attempt_letter+notintheword)))
                regex_result += r"[^"+letterstodrop+r"]{1}"
                print(f"b - {regex_result}")
            if result_letter == "y":
                letterstodrop = ''.join(sorted(set(attempt_letter+notintheword)))
                if f"{i},{attempt_letter}" not in self.misplaced_letters:
                    self.misplaced_letters.append(f"{i},{attempt_letter}")
                regex_result += r"[^"+letterstodrop+r"]{1}"
                print(f"y - {regex_result}")
        compiled_result = re.compile(regex_result)
        print(f"generated regex: {compiled_result}")
        return (required_letters, compiled_result)

    def process_tries(
        self,
    ) -> None:
        """ processes the user input """
        for attempt, res in self.tries:
            trytuple = self.generate_regex(attempt, res)
            if trytuple not in self.regexes:
                print(f"Adding trytuple: {trytuple}")
                self.regexes.append(trytuple)

    def test_word(
        self,
        checkword: str,
    ) -> bool:
        """ tests if a given word is OK, returns a bool """

        for required_letters, regex in self.regexes:
            if regex.search(checkword) is None:
                return False
            for letter in required_letters:
                if letter not in checkword:
                    return False
        return True

    def test_words(self):
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

        for allowed_word in self.allowed_words:
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
        if attempt not in self.wordlist:
            raise ValueError(f"Attempted word {attempt} not in wordlist")
        if len(attempt) != 5:
            raise ValueError(f"Invalid input length, should be 5, got {len(attempt)}")
        if attempt not in self.wordlist:
            raise ValueError(f"Invalid attempt word: {attempt} not in wordlist.")
        return attempt

    def add_try(self, attempted_word: str, result_input: str):
        """ takes an attempt and the result, adds it to the list """
        self.tries.append((
            self.validate_attempt_entry(attempted_word),
            self.validate_result_entry(result_input)))

    def list_tries(self):
        """ lists the attempts """
        for attempt, attempt_result in self.tries:
            print(f"{attempt}\t{attempt_result}")

    def print_results(self) -> bool:
        """ display the things """

        print("Regexes:")
        for regex in self.regexes:
            print(regex)
        if len(self.allowed_words) == 0:
            print("No possible words remain, bailing.")
            sys.exit(1)
        elif len(self.allowed_words) == 1:
            firstword = self.allowed_words[-1]
            print(f"Found word: {firstword}")
            return True
        print("Dumping wordlist")
        scoredlist = sorted((value, key) for (key, value) in self.wordscores.items())
        for score, word in reversed(scoredlist[-5:]):
            print(f"{score} - {word}")
        return False
