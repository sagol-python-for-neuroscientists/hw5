import pathlib
import json
from pydoc import resolve
from typing import Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
                  
        self.data_fname = pathlib.Path(data_fname)
        if not self.data_fname.is_file():
            raise ValueError("ValueError exception thrown")
                
    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """

        f = open(self.data_fname)
        data = pd.read_json(f)

        self.data = data
        
        
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.
        Returns
        -------
        hist : np.ndarray
        Number of people in a given bin
        bins : np.ndarray
        Bin edges
        """
        age_col = self.data['age']
        age_col = age_col.dropna()

        hist, bins = np.histogram(age_col, bins=range(0, 110, 10))

        plt.hist(age_col, bins = range(0, 110, 10)) 
        plt.title("histogram") 
        plt.xlabel('age')
        plt.ylabel('count')
        plt.show()

        return(hist, bins)

    
    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.
        Returns
        -------
        df : pd.DataFrame
        A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
        the (ordinal) index after a reset.
        """
        mails = self.data['email']

        cond_idxs = []
        i = 0
        for ad in mails: 
            cond = all([ad.count('@') == 1, ad.find('@') !=0, ad[::-1].find('@')!=0, 
            ad.count('.')>0, ad.find('.') !=0, ad[::-1].find('.')!=0, ad.count('@.')==0 ])
            if cond is True: 
                cond_idxs.append(i)
                
            i = i+1


        df = self.data.iloc[cond_idxs, :]
        df.index = range(0, 86)
        
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
          
        data = self.data
        data_qs = data[['q1', 'q2', 'q3', 'q4', 'q5']]
        df = data_qs.fillna(data_qs.mean(axis=0)) 
        arr = np.unique(np.where(data_qs.isna())[0])

        return df,arr


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

        data = self.data
        data_qs = data[['q1','q2','q3','q4', 'q5']]
        data['score'] = data_qs.mean(axis = 1)

        nan_count = data_qs.isnull().sum(axis=1)
        i = 0
        for c in nan_count: 
            if c >1 : 
                data.iloc[i,12] = np.NaN
            i = i+1

        data['score'] = np.floor(pd.to_numeric(data['score'], errors='coerce')).astype('UInt8')

        return data



