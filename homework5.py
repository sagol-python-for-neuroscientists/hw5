from typing import Union
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

class QuestionnaireAnalysis:

    def __init__(self, data_fname: Union[Path, str]):
        if type(data_fname) == str:
            try:
                self.data_fname = Path(data_fname)
            except ValueError:
                raise ValueError("input is not valid")
        else:
            self.data_fname = data_fname
        if not self.data_fname.exists():
            raise ValueError("file not found")
        self.data = None
    # if the input is a string, transforms to Path and check validity. than checks if the file exists.

    def read_data(self):
        self.data = pd.read_json(self.data_fname)
    
    def show_age_distrib(self) -> tuple[np.ndarray, np.ndarray]:
        y = np.array(self.data["age"].dropna(axis = 0))
        bins = np.linspace(0, 100, 11)
        hist, out_bins = np.histogram(y,bins = bins)
        return hist, out_bins
    # creates an array from the 'age' column without NaNs, and determine the bins (0,10,20 and so on to 100).
    # than puts in a histogram and returns its values,

    def remove_rows_without_mail(self) -> pd.DataFrame:
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        emails_to_check = list(self.data['email'])
        index = []
        for i,v in enumerate(emails_to_check):
            if not(re.search(regex,v)):
                index.append(i)
        new_data = self.data.drop(labels=index, axis=0).reset_index()
        return new_data
    # using regex checking the validity of each mail.
    # the for loop runs through email adresses and create a list of the indexes of the wrong mails.
    # a new variable is set to contain the dataframe without the unwanted rows and resets the row indexes.

    def fill_na_with_mean(self) -> tuple[pd.DataFrame, np.ndarray]:
        nans_in_quest = np.isnan(self.data.loc[:,'q1':'q5'])
        nans_in_quest = np.array(nans_in_quest.any(axis=1))
        self.data.loc[:,'q1':'q5'].fillna(self.data.loc[:,'q1':'q5'].sum(axis=1), inplace=True)
        return self.data, nans_in_quest
    # created a mask for the rows that contain NaN values in the questionneires section.
    # using fillna method only in the questionneires section to fill the missing values with the row's avarage score.

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        questionneires = self.data.loc[:,'q1':'q5']
        nans_in_quest = questionneires.isna().sum(axis=1) <= maximal_nans_per_sub
        data_to_calculate = questionneires[nans_in_quest]
        data_to_calculate['mean_score'] = data_to_calculate.mean(axis=1)
        self.data['mean_score'] = data_to_calculate['mean_score']
        return self.data
    # creates a copy of the questionneires section, and a mask of the subjects that has as much info as demended.
    # than creates a new dataframe contains only the relevant subjects and calculate their average score
    # adding the avarge values to the original df. the subjects that weren't in the calculation df will get NaN values to this column.