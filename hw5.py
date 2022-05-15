import pathlib

import matplotlib.pyplot as plt
import pandas as pd
from typing import Union, Tuple
import numpy as np


class QuestionnaireAnalysis:  # a new class to read a file as dataframe, and perform data filtration and analyzing it
    def __init__(self, data_fname: Union[pathlib.Path, str]):  # self.data_fname will contain the file name as
        # pathlib.path or string that will be converted into pathlib.path
        try:  # try opening the file
            f = open(data_fname)  # open file
        except EnvironmentError:  # if it does not exist, error will rise
            raise ValueError  # return ValueError to user
        else:  # if it exists
            if type(data_fname) == str:  # if the input was string
                data_fname = pathlib.Path(data_fname)  # turn the input into path file
            self.data_fname = data_fname  # assign the path into self.data_fname

    def read_data(self):  # read the file into self.data
        self.data = pd.read_json(self.data_fname)  # read the data

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:  # create a graph with age distribution and return
        # the histogram and the bins edges
        age_col = self.data['age'].tolist()  # age column is transformed into a list
        hist, bins = np.histogram(age_col, bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # create values to return
        plt.hist(age_col, bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], range=(0, 100))  # create plt hist
        plt.title("Age Histogram")  # hist title
        plt.xlabel("Age")  # hist x-axis name
        plt.ylabel("#N")  # hist y-axis name
        plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # show all these bins in the final histogram
        plt.show()  # show the histogram
        return hist, bins

    def remove_rows_without_mail(self) -> pd.DataFrame:  # filter out of the content the rows with non-valid email
        df = self.data
        df = df[df.email.str.count('@') == 1]  # filter all that contain anything else than one @
        df = df[df.email.str.contains('\\.')]  # filter all that does not contain "."
        df = df[~df.email.str.contains('@.', regex=False)]  # filter all that contains '@' and '.' after
        df = df[~df.email.str.startswith('@')]  # filter all that start with @
        df = df[~df.email.str.endswith('@')]  # filter all that ends with @
        df = df[~df.email.str.startswith('.')]  # filter all that starts with '.'
        df = df[~df.email.str.endswith('.')]  # filter all that ends with '.'
        df = df.reset_index()  # reset the index
        return df

    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:  # fill all na answers to the average of the
        # student's questions
        df = self.data
        df_mean = df[['q1', 'q2', 'q3', 'q4', 'q5']].mean(axis=1)  # df_mean contains the mean of questions in each row
        is_nan = df[['q1', 'q2', 'q3', 'q4', 'q5']].isnull()  # is_nan is location of all nan values in questions
        row_has_NaN = is_nan.any(axis=1)  # the index for rows with nan questions
        for i in range(len(df.index)):  # for loop with the goal of replacing the nan values using row_has_nan with
            # the mean calculated in df_mean
            df.loc[i, ['q1', 'q2', 'q3', 'q4', 'q5']] = \
                df.loc[i, ['q1', 'q2', 'q3', 'q4', 'q5']].fillna(value=df_mean[i])  # replacing each of the rows with
            # the same row where only the nan were replaced using fillna
        arr = df.index[row_has_NaN]  # arr is only the corrected rows index
        return df, arr

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:  # a function for calculating each
        # students mean score and adding it to a new 'score' column. students with more than maximal_nans_per_sub nan
        # values will get nan instead of score
        df = self.data
        m = df[['q1', 'q2', 'q3', 'q4', 'q5']].mean(axis=1)  # calculating the mean of all students
        na = df[['q1', 'q2', 'q3', 'q4', 'q5']].isnull().sum(axis=1)  # na is the number of nan in each row
        m[na > maximal_nans_per_sub] = np.nan  # turn m where na are more than maximal_nans_per_sub into Nan
        m = m.convert_dtypes()  # change data to fit nan
        df["score"] = m.astype('UInt8')  # insert new column as score, with input of calculated m, after converting
        # to correct data type
        return df



