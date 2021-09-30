import sys
import nltk
import ctypes
import argparse
import itertools

import multiprocessing as mp
import decipher.utils.generator as gen

from typing import Any, Final, Optional
from argparse import Namespace
from dataclasses import dataclass
from decipher.utils.singleton import Singleton
from multiprocessing.managers import ValueProxy


@dataclass
class ArgConfigSchema:
    """Store the arguments configuration.

    Args:
        name (str): Name of the argument.
        config (ArgDetails): Details of the argument.

    Example: -
    ```
    ArgConfigSchema(
        name='foo',
        config=ArgConfigSchema.ArgDetails(
            short_arg='-f',
            long_arg='--foo',
            action='store_true',
            help='foo argument description'
        ),
    )
    ```
    """

    name: str

    @dataclass
    class ArgDetails:
        """Store the arguments details.

        Args:
            help (str): Help information.
            long_arg (str): Long argument name.
            short_arg (str): Short argument name.
            action (Optional[str]): Callback when argument executed.
            metavar (Optional[str]): The meta variable to store the value.
            type (Any): The type of the argument value (optional).
        """

        help: str
        long_arg: str
        short_arg: str
        action: Optional[str] = None
        metavar: Optional[str] = None
        type: Any = None

    config: ArgDetails


class DecipherParserThread(argparse.ArgumentParser, metaclass=Singleton):
    """DecipherParse will handle the CLI interface. To run
    this parser call `DecipherParse()` in `__main__`.
    Example:-

    ```python
    from decipher.ui.cli import DecipherParserThread

    if __name__ == "__main__":
        DecipherParserThread()  # This class requires __main__
    ```
    """

    config: Final = [
        ArgConfigSchema(
            name="verbose",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-v",
                long_arg="--verbose",
                action="store_true",
                help="Display verbose-level information",
            ),
        ),
        ArgConfigSchema(
            name="generate_dataset",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-g",
                long_arg="--generate-dataset",
                action="store_true",
                help="generates the default (nltk.corpus) dataset for training",
            ),
        ),
        ArgConfigSchema(
            name="wordlist",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-w",
                long_arg="--word-list",
                action=None,
                metavar="PATH",
                type=str,
                help="specify the word list file",
            ),
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            prog="decipher",
            epilog="Enjoy deciphering! 😄",
            usage="%(prog)s [options] path",
            description="An 💻 Open-Source tool for 🔓 cracking cipher-encrypted files.",
        )

        for arg in self.config:
            if arg.config.action is not None:
                self.add_argument(
                    arg.config.short_arg,
                    arg.config.long_arg,
                    action=arg.config.action,
                    help=arg.config.help,
                )
            else:
                self.add_argument(
                    arg.config.short_arg,
                    arg.config.long_arg,
                    help=arg.config.help,
                    type=arg.config.type,
                    metavar=arg.config.metavar,
                )

        self.args: Namespace = self.parse_args(sys.argv[1:])

        self.verbose: bool = True if self.args.verbose else False

        self.check_generate_dataset_arg_thread()

    def check_generate_dataset_arg_thread(self) -> None:
        """Checks if the user asked to generate the default dataset. (Thread-ready)
        """
        if self.args.generate_dataset:
            mgr: Final = mp.Manager()

            print(
                "Using nltk corpus"
                if self.args.word_list is None
                else f"Using {self.args.word_list}"
            )

            gen.make()
            keys: Final = [list(range(0, 100))] * gen.threads
            corpus_words: Final = gen.split(
                list(nltk.corpus.words.words())
                if self.args.word_list is None
                else list(set(open(self.args.word_list).read().split())),
                splits=gen.threads,
            )

            thread_id: ValueProxy = mgr.Value(ctypes.c_int, 0)

            with mp.Pool(gen.threads) as pool:
                pool.starmap(
                    gen.generate_thread,
                    zip(corpus_words, itertools.repeat(thread_id), keys),
                )
