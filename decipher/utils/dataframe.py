import numpy
import pandas
import sklearn

from typing import Tuple, Any
from vectorizer import DecipherCustomLightWeightVectorizer
from snips import deprecated, Singleton

class DecipherDataFrame(object):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.dataframe = pandas.read_csv(path)
        self.dataframe.columns = ["source", "key", "converted"]

        # Checking for null value and removing rows with null value
        self.dataframe = (
            self.dataframe.dropna()
            if self.dataframe.isnull().any().any()
            else self.dataframe
        )

        self.select_x_and_y()

    def select_x_and_y(self):
        self.x: pandas.DataFrame = self.dataframe["converted"]
        self.y: pandas.DataFrame = self.dataframe["source"]

    def encode(self, quick: bool) -> Tuple[Any, Any]:
        vectorizer = DecipherCustomLightWeightVectorizer(self.dataframe)
        print(vectorizer.converted_dataframe)
        return vectorizer.vectorized_x, vectorizer.labelled_y

    def split(self, quick: bool) -> Tuple[Any, Any, Any, Any]:
        x_encoded, y_encoded = self.encode(quick)

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            x_encoded, y_encoded, test_size=0.3,
        )

        return x_train, x_test, y_train, y_test

    @deprecated
    def pick_properly(self, classes: int, total_keys: int) -> pandas.DataFrame:
        return self.dataframe.head(classes * total_keys)
