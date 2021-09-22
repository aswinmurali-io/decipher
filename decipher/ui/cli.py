import sys
import nltk
import ctypes
import argparse
import itertools

import multiprocessing as mp
import decipher.utils.generator as gen

from typing import Final
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
            action (Union[str, Type[argparse.Action]): Callback when argument executed.
        """

        help: str
        long_arg: str
        short_arg: str
        action: str

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
                help="generates the default dataset for training",
            ),
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            prog="decipher",
            epilog="Enjoy the program! 😄",
            usage="%(prog)s [options] path",
            description="An 💻 Open-Source tool for 🔓 cracking cipher-encrypted files.",
        )

        for arg in self.config:
            self.add_argument(
                arg.config.short_arg,
                arg.config.long_arg,
                action=arg.config.action,
                help=arg.config.help,
            )

        self.args: Namespace = self.parse_args(sys.argv[1:])

        self.verbose: bool = True if self.args.verbose else False

        self.check_generate_dataset_arg_thread()

    def check_generate_dataset_arg_thread(self) -> None:
        """Checks if the user asked to generate the default dataset. (Thread-ready)
        """
        if self.args.generate_dataset:
            mgr: Final = mp.Manager()

            gen.make()
            keys: Final = [list(range(0, 100))] * gen.threads
            corpus_words: Final = gen.split(
                list(nltk.corpus.words.words()), splits=gen.threads
            )

            thread_id: ValueProxy = mgr.Value(ctypes.c_int, 0)

            with mp.Pool(gen.threads) as pool:
                pool.starmap(
                    gen.generate_thread,
                    zip(corpus_words, itertools.repeat(thread_id), keys),
                )
