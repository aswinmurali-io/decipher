import numpy
import pickle
import pandas
import sklearn.preprocessing

from typing import Final
from snips import Singleton
from generator import working_path, dataset_filename, dataset_path

line = 1


def debug_len(x):
    global line
    line += 1
    if type(x) == float:
        print(x, line)
        return 0
    else:
        return len(x)


class DecipherCustomLightWeightVectorizer(object, metaclass=Singleton):
    def __init__(
        self,
        decipher_dataframe_loader,
        csv_path: str = f"{working_path}{dataset_path}{dataset_filename}",
        encrypted_column: str = "converted",
        target_column: str = "source",
    ) -> None:
        super().__init__()

        self.decipher_dataframe = decipher_dataframe_loader

        self.source_encoder: Final = sklearn.preprocessing.LabelEncoder()
        self.encrypted_encoder: Final = sklearn.preprocessing.MinMaxScaler()
        
        self.target_column = target_column

        # Checking for null value and removing rows with null value
        if self.decipher_dataframe.dataframe.isnull().any().any():
            self.decipher_dataframe.dataframe = (
                self.decipher_dataframe.dataframe.dropna()
            )

        # Get the largest string length and fill '-' to the array to match the shape
        self.max_vectorized_length = self.decipher_dataframe.x.map(debug_len).max()

    @property
    def labelled_y(self) -> numpy.ndarray:
        return self.source_encoder.fit_transform(self.decipher_dataframe.y)

    @property
    def vectorized_x(self, fill_character: str = "-") -> numpy.ndarray:
        ascii_array = [
            [ord(character) for character in list(encrypted)]
            for encrypted in self.decipher_dataframe.x
        ]
        processed = []
        for ascii in ascii_array:
            processed.append(
                ascii
                + [ord(fill_character)] * (self.max_vectorized_length - len(ascii))
            )
        return self.encrypted_encoder.fit_transform(processed)

    def save_everything(self) -> None:
        with open("source_encoder.pkl", "wb") as file:
            pickle.dump(self.source_encoder, file)
        with open("encrypted_encoder.pkl", "wb") as file:
            pickle.dump(self.encrypted_encoder, file)
        self.converted_dataframe.to_csv(
            f"{working_path}{dataset_path}final.csv", index=False
        )

    @property
    def converted_dataframe(self) -> pandas.DataFrame:
        feature_columns: Final = [f"V{i}" for i in range(self.max_vectorized_length)]
        processed: Final = pandas.DataFrame(self.vectorized_x, columns=feature_columns)
        processed[self.target_column] = self.labelled_y
        return processed
