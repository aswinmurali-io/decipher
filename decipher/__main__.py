import nltk
import ctypes
import itertools
import multiprocessing as mp
import decipher.utils.generator as gen

from decipher.ui.cli import DecipherParser
from multiprocessing.managers import ValueProxy
from typing import Final


mgr: Final = mp.Manager()

gen.make()
keys: Final = [list(range(0, 100))] * gen.threads
corpus_words: Final = gen.split(list(nltk.corpus.words.words()), splits=gen.threads)

if __name__ == "__main__":
    thread_id: ValueProxy = mgr.Value(ctypes.c_int, 0)

    with mp.Pool(gen.threads) as pool:
        pool.starmap(
            gen.generate_thread, zip(corpus_words, itertools.repeat(thread_id), keys),
        )

    # DecipherParser().parse_args()
