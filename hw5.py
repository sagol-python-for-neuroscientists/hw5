import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns 
import pathlib
from typing import Union, Tuple
import re

data_fname = '/Users/guyweintraub/Desktop/Google Drive/קורסים/Python_course/hw5/data.json'
data = pd.read_json(data_fname)

class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = data_fname

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)

    ####### q1 #######
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.

        Returns
        -------
        hist : np.ndarray
            Number of people in a given bin
        bins : np.ndarray
            Bin edges
            """
        age_bins = list(range(0,101,10))

        fig1, ax1 = plt.subplots()
        hist, bins, _ = ax1.hist(data['age'], bins=age_bins)
        ax1.set_xlabel('Age')

        return hist, bins

    
    ####### q2 #######
    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

        Returns
        -------
        df : pd.DataFrame
            A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
            the (ordinal) index after a reset.
        """
        pattern_valid = '[^@]+@[^@]+\.com$' # structure of valid email adress
        email_filt = self.data['email'].str.match(pattern_valid) # series - boolean filter on rows
        df = self.data[email_filt]
        df.reset_index(drop=True, inplace=True)
        return df


    ####### q3 #######
    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        """Finds, in the original DataFrame, the subjects that didn't answer
        all questions, and replaces that missing value with the mean of the
        other grades for that student.

        Returns
        -------
        df : pd.DataFrame
            The corrected DataFrame after insertion of the mean grade
        arr : np.ndarray
            Row indices of the students that their new grades were generated
            """
        # get arr: all indices of rows with NaN values
        rows_with_nan, _ = np.where(pd.isnull(self.data.loc[:,'q1':'q5']))
        arr = np.unique(rows_with_nan)

        # create a series with means by row
        m = self.data.loc[:,'q1':'q5'].mean(axis=1)
        # loop over columns q1:q5, fill NaN with mean
        for quest in self.data.loc[:,'q1':'q5']:
            self.data.loc[:,quest].fillna(m,inplace=True)
        
        return self.data, arr
    

    ####### q4 #######
    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        """Calculates the average score of a subject and adds a new "score" column
        with it.

        If the subject has more than "maximal_nans_per_sub" NaN in his grades, the
        score should be NA. Otherwise, the score is simply the mean of the other grades.
        The datatype of score is UInt8, and the floating point raw numbers should be
        rounded down.

        Parameters
        ----------
        maximal_nans_per_sub : int, optional
            Number of allowed NaNs per subject before giving a NA score.

        Returns
        -------
        pd.DataFrame
            A new DF with a new column - "score".
        """
        # create a series with means by row
        score = self.data.loc[:,'q1':'q5'].mean(axis=1)
        # find the rows with >2 NaN
        row_nan_count = pd.isnull(self.data.loc[:,'q1':'q5']).sum(axis=1)
        rows_to_NA_bool = row_nan_count > maximal_nans_per_sub
        # turn these rows in score to NaN
        score.loc[rows_to_NA_bool] = np.nan
        # set dtype to UInt8!
        score_rounded_UInt8 = score.apply(np.floor).astype("UInt8")
        # add "score" column to df       
        df = self.data.copy()
        df['score'] = score_rounded_UInt8
        
        return df
  

    ####### q5 - bonus #######
    def correlate_gender_age(self) -> pd.DataFrame:
        """Looks for a correlation between the gender of the subject, their age
        and the score for all five questions.

        Returns
        -------
        pd.DataFrame
            A DataFrame with a MultiIndex containing the gender and whether the subject is above
            40 years of age, and the average score in each of the five questions.
        """


q = QuestionnaireAnalysis(data_fname)
q.read_data()

q2 = q.remove_rows_without_mail()
q3, arr = q.fill_na_with_mean() 

q_a = QuestionnaireAnalysis(data_fname)
q_a.read_data()
q4 = q_a.score_subjects()
q4_more = q_a.score_subjects(0)
q4_x = q_a.score_subjects(2)

# a = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
#                    'B': ['B0', 'B1', 'B2', 'B3'],
#                   'C': ['C0', 'C1', 'C2', 'C3'],
#                    'D': ['D0', 'D1', 'D2', 'D3']},
#                  index=[0, 1, 2, 3])

# e = pd.Series([1,2,3,4])

# new = pd.concat([a,e],axis=1)