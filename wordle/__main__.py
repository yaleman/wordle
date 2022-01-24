""" cli interface """

import click

from . import WordleThing
from .wordlist import wordle_list, second_wordle_list

@click.command()
@click.option("--debug", "-d", is_flag=True)
@click.option("--words", "-w", type=int, default=10, help="Show this many word matches, defaults to 10.")
def cli(debug: bool, words: int):
    """CLI for this thing"""
    wordle = WordleThing(
        wordlist=wordle_list+second_wordle_list,
        debug=debug,
        show_words=words,
        )

    try:
        while True:
            attempt_word = input("Word you tried: ").strip()
            result = input("Result (list of gbyy): ").strip()
            try:
                wordle.add_try(attempt_word, result)
            except ValueError as input_error:
                wordle.logger.error("Input validation error: %s", input_error)
            wordle.process_tries()
            wordle.test_words()
            wordle.generate_wordscores()
            if wordle.print_results():
                return
            wordle.logger.info(
                "You have %s words to choose from.",
                len(wordle.allowed_words),
                )
    except KeyboardInterrupt:
        wordle.logger.error("Quitting...")


if __name__ == "__main__":
    cli() # pylint: disable=no-value-for-parameter
