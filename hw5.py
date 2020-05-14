
import pandas as pd
import numpy as np
import pathlib
from typing import Union 
import matplotlib.pyplot as plt
import re 
plt.close('all')

fname='data.json'

#regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{1,3})+$'
def check(email):      
    if(re.search(regex,email)):
        email=1   
    else:  
        email=0 
    return email 



class QuestionnaireAnalysis:

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        if isinstance(data_fname, pathlib.PurePath):
           self.data_fname=data_fname
        elif isinstance(data_fname, str):
            self.data_fname = pathlib.Path(data_fname)
        
        if self.data_fname.is_file()==False:
            raise ValueError


            
    
    def read_data(self):
        self.data= pd.read_json(self.data_fname)
        return self.data
    

    def remove_rows_without_mail(self) -> pd.DataFrame:
        
        data=self.data
        data['email_check']=data['email']
        counter=0
        for i in data['email']:
            data.loc[counter,'email_check']=check(i)
            #data['email_check'][counter]=check(i)
            counter=counter+1
        w= data[data.email_check != 0]
        self.data=w.reset_index(drop=True)
        
        return self.data
    
    def show_age_distrib(self):
        data=self.data
        binss =np.arange(0,110,10)
        self.ans=np.histogram(data['age'], bins=binss)
        return self.ans

    def fill_na_with_mean(self):
        df=self.data
        df_imp=df.T.fillna(df.loc[:,'q1':'q5'].mean(axis=1)).T
        inds = pd.isnull(df.loc[:,'q1':'q5']).any(1)
        index=np.array(inds.index[inds == True])
        self.ans=(df_imp,index)

        return self.ans
    def score_subjects(self):

        df= self.data
        df['score']=df.loc[:,'q1':'q5'].mean(axis=1).apply(np.floor).astype("UInt8")
        df['nacount']=df.loc[:,'q1':'q5'].isnull().sum(axis=1)
        df.loc[df['nacount']>1, 'score'] = np.nan
        del df['nacount']
        self.data=df

        return self.data





