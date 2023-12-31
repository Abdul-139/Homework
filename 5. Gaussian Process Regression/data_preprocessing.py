# -*- coding: utf-8 -*-
"""Data Preprocessing

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q2r3UZBJ9F4i8VWdSNCMeAaK_YRcFkjV

# 1. Load a dataset
"""

##IMPORTING THE RELEVANT LIBRARIES
import pandas as pd
data = pd.read_csv('https://raw.githubusercontent.com/AjStephan/curcumin/main/PubChem_compound_list.csv')
data.head()

"""# 2. Clean the data"""

# to see missing values
data.isnull().sum()

numerical_data = data.drop(['cmpdname', 'isosmiles', 'mw', 'exactmass', 'monoisotopicmass' ],axis =1)

# Let's simply drop all missing values
# This is not always recommended, however, when we remove less than 5% of the data, it is okay
data_no_mv = numerical_data.dropna(axis=0)

data_no_mv.isnull().sum()

# Descriptive statistics are very useful for initial exploration of the variables
# By default, only descriptives for the numerical variables are shown
# To include the categorical ones, you should specify this with an argument
data_no_mv.describe(include='all')

# Note that categorical variables don't have some types of numerical descriptives
# and numerical variables don't have some types of categorical descriptives

data_no_mv.info()

data_no_mv.columns

cols = ['xlogp', 'polararea', 'heavycnt', 'hbonddonor', 'hbondacc', 'rotbonds']

import seaborn as sns

sns.pairplot(data_no_mv[cols])

data_no_mv.corr()