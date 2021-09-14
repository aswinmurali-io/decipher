import nltk
import itertools
import multiprocessing as mp

from decipher.ui.cli import DecipherParser
from decipher.utils.generator import DatasetGenerator

manager = mp.Manager()
generator = DatasetGenerator()
generator.make()

if __name__ == '__main__':
    thread_id = manager.Value('i', 0)

    with mp.Pool(generator.threads) as pool:
        pool.starmap(
            generator.generate_thread,
            zip(
                [nltk.corpus.words.words()] * generator.threads,
                itertools.repeat(thread_id),
            ),
        )

    DecipherParser().parse_args()
