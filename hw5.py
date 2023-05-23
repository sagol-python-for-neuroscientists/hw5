import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Union
import pathlib
import re


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = pathlib.Path(data_fname)
        if not self.data_fname.exists():
            raise ValueError(f"File {self.data_fname} does not exist.")
        self.data = None


    def read_data(self):
        if not pathlib.Path(self.data_fname).exists():
            raise ValueError(f"File {self.data_fname} does not exist.")
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
        bins = range(0, 101, 10)
        hist, bins = np.histogram(self.data['age'], bins=bins)
        plt.hist(self.data['age'], bins=bins, edgecolor='black')
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Number of Participants')
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
        df = self.data.copy()
        pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        mask = df['email'].apply(lambda x: bool(re.match(pattern, x)))
        df = df[mask].reset_index(drop=True)
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
        question_columns = ['q1', 'q2', 'q3', 'q4', 'q5']
        numeric_df = self.data[question_columns].select_dtypes(include=[np.number])
        rows_with_nan = numeric_df[numeric_df.isnull().any(axis=1)]
        df = self.data.copy()  # Create a copy of the original DataFrame to store the filled values
        for i in rows_with_nan.index:
            df.loc[i, question_columns] = df.loc[i, question_columns].fillna(numeric_df.loc[i].mean())
        arr = rows_with_nan.index.values
        return df, arr
                
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
        #copy dataframe
        df = self.data.copy()
        #create questions object
        question_columns = ['q1', 'q2', 'q3', 'q4', 'q5']
        numeric_data = df[question_columns].select_dtypes(include=[np.number])
        #create a mask of rows with null values in grades then calculates mean of rows of students with all grades present
        mask = numeric_data.isnull().sum(axis=1) <= maximal_nans_per_sub
        df.loc[mask, 'score'] = np.floor(numeric_data[mask].mean(axis=1, skipna=True)).fillna(0).astype('UInt8')

        
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
        # Copied dataframe 
        df = self.data.copy()
        
        #dropping rows with missing values in age column
        df = df.dropna(subset=['age'])
        
        #set a new multiindex
        df.index = pd.MultiIndex.from_arrays([df.index, df['gender'], df['age']], names=('index', 'gender', 'age'))

        # Creating an age_group column based on the age
        df['age'] = df['age'].apply(lambda x: x > 40)

        df.set_index(['gender', 'age'], inplace=True)

        # Calculates the mean of each question separately for each gender and age group
        df = df.groupby(['gender', 'age']).mean()[['q1', 'q2', 'q3', 'q4', 'q5']]

        return df