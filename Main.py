from pathlib import Path
import numpy as np
import pandas as pd
import json
from QuestionnaireAnalysis import QuestionnaireAnalysis
from matplotlib import pyplot as plt


data_path = Path('data.json')
q = QuestionnaireAnalysis(data_path)

q.read_data()


(n,bins) = q.show_age_distrib()
q.score_subjects()
#new,l = q.fill_na_with_mean()
print('h')
