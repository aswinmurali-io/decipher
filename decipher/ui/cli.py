import argparse

from typing import (
    Final,
    Type,
    Union,
)
from dataclasses import dataclass
from decipher.utils.singleton import Singleton


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
            action=None,
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
        action: Union[str, Type[argparse.Action]]

    config: ArgDetails


class DecipherParser(argparse.ArgumentParser, metaclass=Singleton):
    """DecipherParse will handle the CLI interface. To run
    this parser call `DecipherParse().parse_args()`.
    """

    CONFIG: Final = [
        ArgConfigSchema(
            name="verbose",
            config=ArgConfigSchema.ArgDetails(
                short_arg="-v",
                long_arg="--verbose",
                action="",
                help="Display verbose-level information",
            ),
        )
    ]

    def __init__(self) -> None:
        super().__init__(
            prog="decipher",
            epilog="Enjoy the program! 😄",
            usage="%(prog)s [options] path",
            description="An 💻Open-Source tool for 🔓 cracking cipher-encrypted files.",
        )

        for arg in self.CONFIG:
            self.add_argument(
                arg.config.short_arg,
                arg.config.long_arg,
                action=arg.config.action,
                help=arg.config.help,
            )
