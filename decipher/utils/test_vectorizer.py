from typing import Final

from dataframe import DecipherDataFrame
from vectorizer import DecipherCustomLightWeightVectorizer

if __name__ == "__main__":
    vectorizer: Final = DecipherCustomLightWeightVectorizer(
        DecipherDataFrame(".decipher/dataset/repaired.csv")
    )

    # print(vectorizer.vectorized_x)

    # print(vectorizer.labelled_y)

    # print(vectorizer.converted_dataframe)

    vectorizer.save_everything()
