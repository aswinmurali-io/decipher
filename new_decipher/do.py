import os
import sys
import pickle
import logging
import pandas as pd

from typing import Any, Final, Optional


input: Final = " ".join(sys.argv[1:])
path: Final = r"C:\Users\MURALI\Documents\GitHub\decipher\datafull.csv"


def setup_logging() -> logging.Logger:
    """Setup the logger object.

    Returns:
        logging.Logger: Returns the logger object.
    """
    logger: Final = logging.getLogger("Decipher")
    logger.setLevel(logging.DEBUG)

    ch: Final = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def __load_pickle_memory(
    pickled_filename: str, logger: logging.Logger
) -> Optional[Any]:
    logger.info(f"Checking for pickle file from {pickled_filename}...")

    if os.path.exists(pickled_filename):
        logger.info("Loading memory from pickle file.")

        with open(pickled_filename, "rb") as file:
            return pickle.load(file)

    logging.warning(f"Unable to find memory from {pickled_filename}")
    return None


def __load_csv_memory(
    logger: logging.Logger, pickled_file: str
) -> Optional[pd.DataFrame]:
    logger.info(f"Found memory from {path}.")
    logger.info("Loading might take time...")

    if os.path.exists(path):
        df: Final = pd.read_csv(path)

        logger.info("Load complete. Generating .pickle file...")

        with open(pickled_file, "wb") as file:
            pickle.dump(df, file)

        return df

    return None


def cache_or_load_memory(logger: logging.Logger) -> pd.DataFrame:
    base: Final = os.path.splitext(path)[0]
    pickled_file: Final = f"{base}.pickle"

    logger.info(f"Loading memory from {path}...")

    # Check for .pickle file first.
    logger.info("Checking for pickle file for better performance instead!")
    df = __load_pickle_memory(pickled_file, logger)

    if df is None:
        # If no .pickle file then, Check for .csv file.
        df = __load_csv_memory(logger, pickled_file)

    if df is None:
        # If no .csv and no .pickle then notify critical error.
        logger.critical(f"Unable to find memory from {path}.")
        return pd.DataFrame()

    return df


def main() -> None:
    logger = setup_logging()

    df: Final = cache_or_load_memory(logger)

    logger.info(f"Memory loaded. Size is {sys.getsizeof(df)} bytes.")

    df.head()

    print(input)


if __name__ == "__main__":
    main()
