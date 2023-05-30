from typing import Tuple
import json
import pathlib 
from typing import Union
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import pdb


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        if isinstance(data_fname, str):
            data_fname = pathlib.Path(data_fname)
        if not isinstance(data_fname, pathlib.Path):
            raise TypeError('data_fname must be a string or a pathlib.Path object')
        if not data_fname.exists():
            raise ValueError('data_fname does not exist')
        self.data_fname = data_fname
        self.data = None
        

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)


    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.

        Returns
        -------
        hist : np.ndarray
            Number of people in a given bin
        bins : np.ndarray
            Bin edges
        """
        # Convert the data to a DataFrame
        df = pd.DataFrame(self.data)

        # Plot the histogram
        hist, bins, _ = plt.hist(df['age'], bins=10, range=(0, 100))
        plt.show()

        return hist, bins


    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

        Returns
        -------
        df : pd.DataFrame
            A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
            the (ordinal) index after a reset.
        """
        # Convert the data to a DataFrame
        df = pd.DataFrame(self.data)

        # Filter rows with invalid emails, using a boolean mask
        valid_email_mask = df['email'].apply(lambda x: bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', x)))
        df = df[valid_email_mask]

        # Reset the index
        df.reset_index(drop=True, inplace=True)

        return df


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
        # Convert the data to a DataFrame
        df = pd.DataFrame(self.data)
        # search for rows with missing values, only in the questions columns (q1-q5)
        missing_values_mask = df[['q1', 'q2', 'q3', 'q4', 'q5']].isnull().any(axis=1)
        # Iterate over the missing rows and fill missing values with mean, while ignoring strings
        for i in df[missing_values_mask].index:
            df.loc[i, 'q1':'q5'] = df.loc[i, 'q1':'q5'].apply(lambda x: np.mean(df.loc[i, 'q1':'q5']) if type(x) is int else x)
        # Get the row indices of the corrected grades
        corrected_indices = df[missing_values_mask].index
             
        return df, corrected_indices

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
        # Convert the data to a DataFrame
        df = pd.DataFrame(self.data)
        # Calculate the average score per subject
        df['score'] = df[['q1', 'q2', 'q3', 'q4', 'q5']].mean(axis=1)
        # Filter subjects with more than maximal_nans_per_sub NaNs
        df.loc[df[['q1', 'q2', 'q3', 'q4', 'q5']].isnull().sum(axis=1) > maximal_nans_per_sub, 'score'] = np.nan
        # round the score down
        df['score'] = df['score'].apply(lambda x: np.floor(x))
        # convert the score column to UInt8
        df['score'] = df['score'].astype('UInt8')

        return df


    def correlate_gender_age(self) -> pd.DataFrame:
        """Looks for a correlation between the gender of the subject, their age
        and the score for all five questions.

        Returns
        -------
        pd.DataFrame
            A DataFrame with a MultiIndex containing the gender and whether the subject is above
            40 years of age, and the average score in each of the five questions.
        """
        # Convert the data to a DataFrame
        df = pd.DataFrame(self.data)

        # Transform the index into a MultiIndex with three levels
        df.set_index([df.index, 'gender', pd.cut(df['age'], [0, 40, np.inf], labels=['Below 40', 'Above 40'])], inplace=True)

        # Group the subjects based on gender and age
        groups = df.groupby(['gender', 'age'])

        # Calculate the average result per question per group
        average_scores = groups[['q1', 'q2', 'q3', 'q4', 'q5']].mean()

        return average_scores








 