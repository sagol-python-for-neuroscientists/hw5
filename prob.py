from typing import Union
import pathlib 
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt  
import numpy as np
import json
import math


wanted_folder=2
current_folder = Path().absolute() # path of the current folder
foldernamepath = pathlib.Path('teststs.fdfd') # path of the wanted folder



fname = pathlib.Path(__file__)
#q = QuestionnaireAnalysis(fname)

#print(q.read_data())

#data_df = pd.read_json(fname) # Load the file
#self.data=data_df # Saving the data to a the attribute self.data

#print(fname)
#print(data_df)

#f = open(fname) 
#data = json.load(f) 

new_df=pd.DataFrame( index =['first', 'second'], columns =['q1', 'q2','q3','q4','q5'])
new_df.loc['first']=[1,2,3,4,5]
#print(new_df)

#print(type(np.array([math.floor(1.5)])))
number_of_nan=[1,2,3,4]

for idx, num in enumerate(number_of_nan):
    print(num)
    print(idx)



for x in [1,2]:
    print(x)


 #   def score_subjects(self, maximal_nans_per_sub: int = 1):
  #      """Calculates the average score of a subject and adds a new "score" column
 #       with it.

 #       If the subject has more than "maximal_nans_per_sub" NaN in his grades, the
 #       score should be NA. Otherwise, the score is simply the mean of the other grades.
 #       The datatype of score is UInt8, and the floating point raw numbers should be
  #      rounded down.
#
  #      Parameters
 #       ----------
  #      maximal_nans_per_sub : int, optional
  #      Number of allowed NaNs per subject before giving a NA score.
#
   #     Returns
   #     -------
   #     A new DF with a new column - "score".
    #    """
   #     data_df=self.read_data() # Put the data into a data frame
   #     questions_ans=data_df.loc[:, 'q1':'q5'] # Indexes of the wanted columns
  #      number_of_nan=questions_ans.isnull().sum(axis=1).tolist()
  #      floored_mean_score=np.floor(questions_ans.mean(axis=1).astype(np.uint8)

        
        
       #  for idx, num in enumerate(number_of_nan):
       #      if num>maximal_nans_per_sub:
       #         floored_mean_score[idx]='NA'
       #      else:
       #          continue
        
       # data_df['score']=floored_mean_score #.astype('pd.UInt8Dtype').dtypes


def cat()