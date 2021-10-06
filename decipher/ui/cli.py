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
from decipher.utils.generator import dataset_filename
from decipher.utils.snips import Singleton
from decipher.utils.loader import DecipherModelLoader
from decipher.experimental.model_v1 import DecipherModel
from multiprocessing.managers import ValueProxy
from caesarcipher import CaesarCipher
from Cryptokit.VigenereCipher import v_dictionaryattack


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
                help="display verbose-level information",
            ),
        ),
        ArgConfigSchema(
            name="generate_dataset",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-g",
                long_arg="--generate-dataset",
                action="store_true",
                help="generates the dataset for training",
            ),
        ),
        ArgConfigSchema(
            name="quick_train",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-qt",
                long_arg="--quick-train",
                action="store_true",
                help="quickly train the model by reducing complexity",
            ),
        ),
        ArgConfigSchema(
            name="train_model",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-t",
                long_arg="--train-model",
                action="store_true",
                # TODO: change this to support multi-model support
                help="train the model (uses model_v1)",
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
                help="specify the word list file, default is nltk.corpus",
            ),
        ),
        ArgConfigSchema(
            name="brute",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-b",
                long_arg="--boost",
                action="store_true",
                help="",
            ),
        ),
        ArgConfigSchema(
            name="input_file",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-if",
                long_arg="--input-file",
                action=None,
                metavar="PATH",
                type=str,
                help="specify the file 📄 to crack 🔑",
            ),
        ),
        ArgConfigSchema(
            name="input",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-i",
                long_arg="--input",
                action=None,
                metavar="TEXT",
                type=str,
                help="specify the text 🅰 to crack 🔑",
            ),
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            prog="decipher",
            epilog="Enjoy deciphering! 😄",
            usage="%(prog)s [options] path",
            description="An 💻 open-source tool for 🔓 cracking cipher-encrypted files.",
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
        if not self.args.brute:
            self.check_input()
        else:
            self.check_input_for_brute()
        self.check_train()

    def check_input_for_brute(self) -> None:
        print(CaesarCipher(self.args.input).cracked)
        # print(v_dictionaryattack(self.args.input))

    def check_train(self) -> None:
        if self.args.train_model:
            path: Final = f".decipher/dataset/{dataset_filename}"
            print(f"Started training from dataset {path}")
            model = DecipherModel()
            print(f"Pickling to {model.model_file}")
            if self.args.quick_train is not None:
                print("Quick train is enabled")
            model.train(
                path,
                total_classes=1000,
                total_keys=100,
                quick=True if self.args.quick_train is not None else False,
            )
            model.save()

    def check_input(self) -> None:
        if self.args.input is not None or self.args.input_file is not None:
            loader = DecipherModelLoader()
            result = loader.load()
            if result is not None:
                model, encrypted_encoder, source_encoder = result
                print(model)
            if result is None:
                print("Found no model!")
                return
            if self.args.input is not None and model is not None:
                print(model.run(self.args.input.split(" ")))
            elif self.args.input_file is not None and model is not None:
                with open(self.args.input_file) as file:
                    print(" ".join(model.run(file.read().split())))

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
