"""
Generates cipher encoded dataset for decipher.

Example: -

```python
import itertools
import multiprocessing as mp
import decipher.utils.generator as gen

mgr: Final = mp.Manager()

# Setup the dataset path
gen.make()

keys: Final = gen.split(range(0, 100), splits=gen.threads)
corpus_words: Final = gen.split(nltk.corpus.words.words(), splits=gen.threads)

if __name__ == "__main__":
    thread_id: ValueProxy = mgr.Value(ctypes.c_int, 0)

    with mp.Pool(gen.threads) as pool:
        pool.starmap(
            gen.generate_thread, zip(corpus_words, itertools.repeat(thread_id), keys),
        )
```

Refer`generate_thread(...)`function for more information
on the generating process parameter(s).
"""

import os
import numpy

from caesarcipher import CaesarCipher

from typing import Any, Iterable, List
from multiprocessing.managers import ValueProxy


threads: int = os.cpu_count() or 1
working_path: str = ".decipher/"
dataset_path: str = "dataset/"
dataset_filename: str = "data.csv"


def make() -> None:
    """Setup the decipher's dataset folder."""

    if not os.path.exists(working_path):
        os.mkdir(working_path)

    if not os.path.exists(f"{working_path}{dataset_path}"):
        os.mkdir(f"{working_path}{dataset_path}")

    if os.path.exists(f"{working_path}{dataset_path}/{dataset_filename}"):
        os.remove(f"{working_path}{dataset_path}/{dataset_filename}")


def split(iteratable: Iterable, splits: int = 1) -> Iterable[List[Any]]:
    """Split any iterable into thread-ready individual iterables.

    Args:
        iteratable (Iterable): The iteratable variable that needs thready-ready split.
        splits (int, optional): Number of splits to be done on the iterable. Defaults to 1.

    Returns:
        Iterable[List[Any]]: Returns the thread-ready split of the iteratable.
    """
    return numpy.array_split(iteratable, splits)


def generate_thread(ciphers: List[str], thread_id: ValueProxy, keys: List[int]) -> None:
    """
    Generate the dataset (thread-ready).

    Args:
        ciphers (List[str]): List of words that needs to encrypted.
        thread_id (ValueProxy[int]): Shareable int variable for identifying threads.
        keys (List[int]): List of keys to generate the encrypted words.
    """

    assert os.path.exists(
        f"{working_path}{dataset_path}"
    ), """
        Dataset directory does not exist. Please make one by calling
        the `make()` function.

        Refer `make()` for more details.
        """

    thread_id.value += 1
    print(f"Started thread {thread_id.value}")

    with open(f"{working_path}{dataset_path}/{dataset_filename}", "a") as csv:
        for word in ciphers:
            for key in keys:
                result = CaesarCipher(word, offset=key).encoded
                print(
                    f"thread={thread_id.value}, word={word}, key={key}, cipher={result}",
                    end="\r",
                )
                csv.write(f"{word},{key},{result}\n")

    # Alert when done
    print("\a")
