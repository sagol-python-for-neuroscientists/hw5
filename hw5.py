# Assignment 5 - Shoval Shahab

from typing import Tuple, Union
import pathlib as pl
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import re
import array
from pandas import UInt8Dtype

class QuestionnaireAnalysis:

    def __init__(self, data_fname: Union[pl.Path, str]):
        if isinstance(data_fname, str):
            data_fname = pl.Path(data_fname)
        if not data_fname.exists():
            raise ValueError("File does not exist.")
        self.data_fname = data_fname
        self.data = None

    def read_data(self):
        self.data = pd.read_json(self.data_fname)
        return self.data

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        df = pd.DataFrame(self.data)
        age_values = pd.to_numeric(df['age'], errors='coerce')
        age_values = age_values.dropna().astype(int)
        bins = [10 * i for i in range(11)]
        hist, bins = np.histogram(age_values, bins=bins)
        return hist, bins
    
    def remove_rows_without_mail(self) -> pd.DataFrame:
        df = self.data.copy()
        email_pattern = r'^[^@\s]+@[^@\s]+(?:\.[^@\s.]+)+$'
        valid_email_mask = df['email'].apply(lambda email: bool(re.match(email_pattern, email)))
        df = df[valid_email_mask].reset_index(drop=True)
        return df


    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        df = self.data
        filled_rows = []
        average = []
        
        def calculate_mean(row):
            av = row[['q1','q2','q3','q4','q5']].dropna().mean()
            average.append(av)
            return row
        
        def replace_nan(row):
            if row[['q1','q2','q3','q4','q5']].isnull().any():
                row[row.isnull()]=average[row.name]
                filled_rows.append(row.name)
            return row

        df = df.apply(calculate_mean, axis=1)
        df = df.apply(replace_nan, axis=1)
        arr = np.array(filled_rows)
        return df, arr

       
    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        df = self.data
        average = []

        def calculate_mean(row):
            av = row[['q1','q2','q3','q4','q5']].dropna().mean()
            av = av.astype(np.uint8)
            average.append(av)
            return row
        
        def condition_maximal_nans_per_sub(row):
            if row[['q1','q2','q3','q4','q5']].isnull().sum() > maximal_nans_per_sub:
                return np.nan
            else:
                return average[row.name].astype(np.uint8)
            
        df = df.apply(calculate_mean, axis=1)
        average = np.array(average)
        arr = df.apply(condition_maximal_nans_per_sub, axis=1)
        arr = pd.array(arr, dtype=np.uint8) 
        df['score'] = arr.astype("UInt8")
        return df


# if __name__ == '__main__':
#     truth = pd.read_csv('tests_data/q4_score.csv', index_col=0).astype("UInt8")
#     fname = 'data.json'
#     q = QuestionnaireAnalysis(fname)
#     q.read_data()
#     df = q.score_subjects()
#     print(df['score'])
#     print("truth: ", truth)
#     a = df["score"].equals(truth)
#     print("aaaaaa: ", a)


    