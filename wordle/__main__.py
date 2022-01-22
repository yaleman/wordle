""" cli interface """

from . import WordleThing
from .wordlist import wordle_list, second_wordle_list

def cli():
    """CLI for this thing"""
    wordle = WordleThing(wordlist=wordle_list+second_wordle_list)

    try:
        while True:
            attempt_word = input("Word you tried: ").strip()
            result = input("Result (list of gbyy): ").strip()
            try:
                wordle.add_try(attempt_word, result)
            except ValueError as input_error:
                print(f"Input validation error: {input_error}")
            wordle.process_tries()
            wordle.test_words()
            wordle.generate_wordscores()
            wordle.print_results()
            print(f"You have {len(wordle.allowed_words)} words")
    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    cli()
