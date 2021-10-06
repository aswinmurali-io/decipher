from dataframe import DecipherDataFrame
from generator import working_path, dataset_path, dataset_filename


class DecipherRepairDataFrame(object):
    def __init__(
        self,
        decipher_dataframe: DecipherDataFrame = DecipherDataFrame(
            path=f"{working_path}{dataset_path}/{dataset_filename}"
        ),
    ) -> None:
        self.decipher_dataframe = decipher_dataframe

        self.__corrupted_lines: list = []
        self.__lines: int = 1

        self.drop_null_values()
        self.check_for_corrupted_rows()

    def drop_null_values(self) -> None:
        # Checking for null value and removing rows with null value
        if self.decipher_dataframe.dataframe.isnull().any().any():
            self.decipher_dataframe.dataframe = (
                self.decipher_dataframe.dataframe.dropna()
            )

    def __debug_rows(self, x):
        self.__lines += 1
        if type(x) != str:
            print(x, self.__lines)
            self.__corrupted_lines.append(self.__lines)
            return 0
        else:
            return len(x)

    def check_for_corrupted_rows(self) -> None:
        self.__lines = 0
        self.decipher_dataframe.x.map(self.__debug_rows).max()
        self.decipher_dataframe.dataframe.drop(self.__corrupted_lines)

    def save(self, filename: str = f"{working_path}{dataset_path}/repaired.csv") -> None:
        self.decipher_dataframe.dataframe.to_csv(filename, index=False)


if __name__ == "__main__":
    repair = DecipherRepairDataFrame()
    repair.save()
