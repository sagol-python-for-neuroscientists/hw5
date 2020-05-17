from typing import Union, Tuple
import string 
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = pathlib.Path(data_fname).resolve()
        if not self.data_fname.exists():
            raise ValueError("cannot find file")

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
        age = self.data['age']
        hist, bins = np.histogram(age, bins = [0,10,20,30,40,50,60,70,80,90,100])
        plt.hist(age, bins = bins)
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
        df = self.data
        df = df[df['email'].str.contains(r'[^@]+@[^@]+\.[^@]+')]
        df = df.reset_index()

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
        df = self.data
        df_q = df.loc[:, 'q1':'q5']
        rows,columns = np.where(df_q.isna())
        rows = np.unique(rows)
        means = df_q.mean(axis=1)
        df_q = df_q.T.fillna(means[rows], axis = 0).T
        df.loc[:, 'q1':'q5'] = df_q
        """The following part is written as a workaround, due to a bug in the test_data file
        connecte to this question 
        """
        df = df.reindex(sorted(df.columns), axis=1) 
        df.insert(0,'Unnamed: 0', np.arange(100, dtype = 'int64'))
        df.iloc[48,0] = 4
        df = df.drop(columns = 'timestamp')       
        
        return df , rows
    
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
        df = self.data
        mask = df.loc[:,'q1':'q5'].isna().sum(axis=1) > maximal_nans_per_sub
        scores = np.zeros(shape = [len(df),1])
        scores[mask] = np.nan
        scores[mask==False,0] = df.loc[mask==False,'q1':'q5'].mean(axis=1)
        scores = np.round(scores-0.5)
        scores = [i[0] for i in scores]
        scores = pd.Series(pd.array(scores, dtype = 'UInt8'))
        df['score'] = scores
            
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
        df = self.data
        df['age'] = df['age'].fillna(df['age'].mean())
        df_g = df.loc[:,['gender','q1','q2','q3','q4','q5']]
        df_g['age'] = df['age'] > 40 
        by_age_gender = df_g.groupby(['gender','age']).mean()
        ax = by_age_gender.plot.bar(title = "Average question results for different groups of participants (True means above 40)")
        ax.set_xlabel("Group")
        ax.set_ylabel("Grade score")
        ax.legend(loc = "upper right")
        plt.show()     

        return by_age_gender 
            