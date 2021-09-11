"""
Generates cipher encoded dataset for decipher.
"""

import os

from typing import List
from decipher.utils.singleton import Singleton
from multiprocessing.managers import ValueProxy


class DatasetGenerator(metaclass=Singleton):
    """
    `DatasetGenerator()`class generates the dataset for
    decipher.

    Example: -

    ```python
    import itertools
    import multiprocessing as mp
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
    ```

    Refer`generate_thread(...)`function for more information
    on the generating process parameter(s).
    """

    threads: int = os.cpu_count() or 1
    working_path: str = '.decipher/'
    dataset_path: str = 'dataset/'

    def __init__(self) -> None:
        super().__init__()

    def make(self) -> None:
        """Setup the decipher's dataset folder."""

        if not os.path.exists(self.working_path):
            os.mkdir(self.working_path)

        if not os.path.exists(f'{self.working_path}{self.dataset_path}'):
            os.mkdir(f'{self.working_path}{self.dataset_path}')

    def generate_thread(self, ciphers: List[str], thread_id: ValueProxy) -> None:
        """
        Generate the dataset (thread-ready).

        Args:
            ciphers (List[str]): List of words that needs to encrypted.
            thread_id (ValueProxy): Shareable int variable for identifying threads
        """

        assert os.path.exists(f'{self.working_path}{self.dataset_path}'), \
            """
            Dataset directory does not exist. Please make one by calling
            the `DatasetGenerator.make()` function.

            Refer `DatasetGenerator.make()` for more details.
            """

        thread_id.value += 1
        print(f"Started thread {thread_id.value}")
        print(ciphers[0])
