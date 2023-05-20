import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple, Union

class QuestionnaireAnalysis:
    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = pathlib.Path(data_fname)
        if not self.data_fname.exists():
            raise ValueError(f"File {self.data_fname} does not exist.")

    def read_data(self):
        self.data = pd.read_json(self.data_fname)

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        ages = self.data['age'].dropna()
        hist, bins = np.histogram(ages, bins=np.arange(0, 101, 10))
        return hist, bins

    def _is_valid_email(self, email: str) -> bool:
        if "@" not in email or "." not in email:
            return False
        if email.endswith(".") or email.endswith("@"):
            return False
        if email.startswith(".") or email.startswith("@"):
            return False
        if not email.isascii() or email.count("@") != 1:
            return False
        if email[email.find("@") + 1] == ".":
            return False
        return True

    def remove_rows_without_mail(self) -> pd.DataFrame:
        return self.data[self.data["email"].apply(self._is_valid_email)].reset_index(drop=True)

    def _find_rows_with_nulls(self) -> np.ndarray:

        only_grades = self.data.loc[:, "q1":"q5"]
        rows_with_nulls = only_grades.loc[
            only_grades.isna().any(axis=1)
        ].index.to_numpy()
        return rows_with_nulls

    def _fill_na_with_mean(self) -> pd.DataFrame:

        only_grades = self.data.loc[:, "q1":"q5"]
        only_means = only_grades.mean(axis=1)
        only_means = pd.DataFrame(
            {key: only_means for key in only_grades.columns}
        )
        only_grades = only_grades.where(only_grades.notnull(), only_means)
        return only_grades

    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:

        rows_with_nulls = self._find_rows_with_nulls()
        only_grades = self._fill_na_with_mean()
        updated = self.data.copy()
        updated.loc[:, "q1":"q5"] = only_grades
        return updated, rows_with_nulls

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        self.data["score"] = self.data.loc[:, "q1":"q5"].mean(axis=1).apply(np.floor).astype("UInt8")
        self.data.loc[self.data.loc[:, "q1":"q5"].isna().sum(axis=1) > maximal_nans_per_sub, "score"] = pd.NA
        return self.data


    def correlate_gender_age(self) -> pd.DataFrame:

        df_clean = self.data.dropna(subset=["age", "gender"])

        df_clean['gender'] = df_clean['gender'].astype(str)

        df_clean.set_index(["gender", "age"], append=True, inplace=True)

        groups = df_clean.groupby([df_clean.index.get_level_values('gender'), df_clean.index.get_level_values('age') > 40])

        result = groups[['q1', 'q2', 'q3', 'q4', 'q5']].mean()

        result.index.names = ['gender', 'age']

        result.sort_index(inplace=True)

        return result
