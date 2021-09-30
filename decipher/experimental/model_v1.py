from sklearnex import patch_sklearn

patch_sklearn()

import os
import numpy
import pickle
import pandas
import sklearn

import sklearn.tree
import sklearn.preprocessing
import sklearn.feature_extraction.text

from typing import Any, Final, Tuple

numpy.random.seed(0)


class DecipherDataFrame(object):
    def __init__(self, path: str, total_classes: int, total_keys: int) -> None:
        super().__init__()
        self.dataframe = pandas.read_csv(path)
        self.dataframe.columns = ["source", "key", "converted"]

        # Checking for null value and removing rows with null value
        self.dataframe = (
            self.dataframe.dropna()
            if self.dataframe.isnull().any().any()
            else self.dataframe
        )

        # Selecting the dataset properly
        self.dataframe = self.pick_properly(
            classes=total_classes, total_keys=total_keys
        )

        self.select_x_and_y()
        self.encode()

    def select_x_and_y(self):
        self.x = self.dataframe["converted"]
        self.y = self.dataframe["source"]

    def encode(self) -> Tuple[Any, numpy.ndarray]:
        self.encrypted_encoder = sklearn.feature_extraction.text.TfidfVectorizer()
        # self.source_encoder = sklearn.preprocessing.LabelEncoder()
        self.source_encoder = sklearn.feature_extraction.text.TfidfVectorizer()

        x_encoded = self.encrypted_encoder.fit_transform(self.dataframe["converted"])
        y_encoded = self.source_encoder.fit_transform(self.dataframe["source"])

        return x_encoded, y_encoded

    def split(self) -> Tuple[Any, Any, Any, Any]:
        x_encoded, y_encoded = self.encode()

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            x_encoded, y_encoded, test_size=0.3,
        )

        return x_train, x_test, y_train, y_test

    def pick_properly(self, classes: int, total_keys: int) -> pandas.DataFrame:
        return self.dataframe.head(classes * total_keys)


class DecipherModel(sklearn.tree.DecisionTreeClassifier):
    model_file: str = "model.pkl"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def train(self, path: str, total_classes: int, total_keys: int):
        self.dataframe = DecipherDataFrame(
            path=path, total_classes=total_classes, total_keys=total_keys,
        )

        x_train, x_test, y_train, y_test = self.dataframe.split()

        self.fit(x_train, y_train)
        self.get_performance(x_test, y_test)

    def get_performance(self, x_test, y_test) -> None:
        y_prediction = self.predict(x_test)
        accuracy = sklearn.metrics.accuracy_score(y_test, y_prediction)
        f1_score = sklearn.metrics.f1_score(y_test, y_prediction, average="weighted")
        print(f"Accuracy {round(accuracy, 2)}, F1-Score {round(f1_score, 2)}")
        print(sklearn.metrics.confusion_matrix(y_test, y_prediction))

    def save(self) -> None:
        with open(self.model_file, "wb") as file:
            pickle.dump(self, file)

    def load(self) -> sklearn.tree.DecisionTreeClassifier:
        with open(self.model_file, "rb") as fid:
            return pickle.load(fid)

    def run(self, encrypted_text: str):
        return self.dataframe.source_encoder.inverse_transform(
            self.predict(self.dataframe.encrypted_encoder.transform([encrypted_text]))
        )


if __name__ == "__main__":
    path: Final = r"../../../decipher/.decipher/dataset/nltk-corpus.csv"

    model = DecipherModel()

    if os.path.exists(f"../../../decipher/decipher/experimental/{model.model_file}"):
        model = model.load()
    else:
        model.train(path, total_classes=1000, total_keys=100)
        model.save()
    print(model.run("apple"))
