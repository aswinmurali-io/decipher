import os
import sys

from typing import Final, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

from decipher.experimental.model_v1 import DecipherModel


class DecipherModelLoader(object):
    def __init__(self) -> None:
        self.model: Optional[DecipherModel] = DecipherModel()
        self.source_encoder: Optional[TfidfVectorizer] = None
        self.encrypted_encoder: Optional[TfidfVectorizer] = None
        self.paths: Final = [
            self.model.model_file,
            f"experimental/{self.model.model_file}",
            f"decipher/experimental/{self.model.model_file}",
            f"decipher/decipher/experimental/{self.model.model_file}",
            f"../../../decipher/decipher/experimental/{self.model.model_file}",
        ]

    def load(
        self,
    ) -> Tuple[
        Optional[DecipherModel], Optional[TfidfVectorizer], Optional[TfidfVectorizer]
    ]:
        if self.model is not None:
            for path in self.paths:
                print(f"Checking {path} for model")
                if os.path.exists(path):
                    print(f"Found at {path}")
                    try:
                        self.model.model_file = path
                        self.model = self.model.load()
                        return (
                            self.model,
                            self.model.dataframe.encrypted_encoder,
                            self.model.dataframe.source_encoder,
                        )
                    except FileNotFoundError as e:
                        sys.stderr.write(f"{str(e)}\n")
        return None, None, None


if __file__ == "__main__":
    loader = DecipherModelLoader()
    if loader is not None and loader.load() is not None:
        model, encrypted_encoder, source_encoder = loader.load()

    if model is not None:
        print(model.run(["apple"]))
