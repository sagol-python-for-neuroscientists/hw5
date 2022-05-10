from asyncore import read
from email import message
from itertools import count
import json
import pandas as pd
import numpy as np
import scipy as sp
from typing import Union
from typing import Tuple
from matplotlib import pyplot as mpl
import pathlib
import pytest

class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        """
        Initialize a questionnare analysis
        """
        BAD_TYPE_MESSAGE = "Invalid input: ({value1})! Only Path or str are accepted"
        BAD_FNAME_MESSAGE= "Invalid input: ({value1})! File not found"
        if not pathlib.Path.exists(pathlib.Path(data_fname)):
            message=BAD_FNAME_MESSAGE.format(value1=data_fname)
            raise ValueError(message)
        if isinstance(data_fname,pathlib.Path):
            self.data_fname=data_fname
        elif isinstance(data_fname,str):
            self.data_fname=pathlib.Path(data_fname)
        else:
            message=BAD_TYPE_MESSAGE.format(value1=data_fname)
            raise TypeError(message)
        

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        with open(self.data_fname,'r') as file:
            self.data=pd.DataFrame(json.load(file))

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.

        Returns
        -------
        hist : np.ndarray
            Number of people in a given bin
        bins : np.ndarray
            Bin edges
        """
        bins=[0,10,20,30,40,50,60,70,80,90,100]
        lent=len(self.data)
        ages=list()
        for n in range(lent):
            age=self.data["age"][n]
            if isinstance(age,int):
                ages.append(age)

        mpl.figure()
        histogram=mpl.hist(ages, bins)
        mpl.show()
        return histogram
    
    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

        Returns
        -------
        df : pd.DataFrame
            A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
            the (ordinal) index after a reset.
        """
        cor_df=self.data
        lent=len(self.data)
        for n in range(lent):
            email=self.data["email"][n]
            email_last_idx=len(email)-1
            if email.find('@')==-1 or  email.find('@')==0 or email.find('@')==email_last_idx:
                cor_df=cor_df.drop(index=n)
                continue
            if not email.find('@')==email.rfind('@'):
                cor_df=cor_df.drop(index=n)
                continue
            if  email.find('.')==-1 or email.find('.')==0 or email.find('.')==email_last_idx:
                cor_df=cor_df.drop(index=n)
                continue
            if not email.find('@.')==-1:
                cor_df=cor_df.drop(index=n)
                continue
        cor_df=cor_df.reset_index()
        return cor_df

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
        df=self.data
        lent=len(self.data)
        corrected=pd.Series(range(lent))
        for n in range(lent):
            cor_flag=False
            q1=float(df['q1'][n])
            q2=float(df['q2'][n])
            q3=float(df['q3'][n])
            q4=float(df['q4'][n])
            q5=float(df['q5'][n])
            meanq=np.nanmean([q1,q2,q3,q4,q5])
            if np.isnan(q1):
                cor_flag=True
                df["q1"][n]=meanq
            if np.isnan(q2):
                cor_flag=True
                df["q2"][n]=meanq
            if np.isnan(q3):
                cor_flag=True
                df["q3"][n]=meanq
            if np.isnan(q4):
                cor_flag=True
                df["q4"][n]=meanq
            if np.isnan(q5):
                cor_flag=True
                df["q5"][n]=meanq
            if not cor_flag:
                corrected=corrected.drop(n)

        return [df,np.array(corrected)]

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

        df=self.data
        lent=len(self.data)
        scores=pd.Series(lent)
        for n in range(lent):
            q1=float(df['q1'][n])
            q2=float(df['q2'][n])
            q3=float(df['q3'][n])
            q4=float(df['q4'][n])
            q5=float(df['q5'][n])
            q_list=[q1,q2,q3,q4,q5]
            num_nan=q_list.count("nan")
            if num_nan<maximal_nans_per_sub:
                scores[n]=np.uint8(np.nanmean([q1,q2,q3,q4,q5]))
            else:
                scores[n]=pd.NA
        df['score']=scores
        return df

truth = pd.read_csv('tests_data/q4_score.csv', squeeze=True, index_col=0).astype("UInt8")
fname = 'data.json'
q = QuestionnaireAnalysis(fname)
q.read_data()
df = q.score_subjects()
print(df["score"])
print(truth)