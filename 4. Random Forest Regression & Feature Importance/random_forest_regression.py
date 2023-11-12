# -*- coding: utf-8 -*-
"""Random Forest Regression

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lf9dSVV1o1qvYDOYunUG6j16wHxg6EWv

# 1. Load a dataset
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import statsmodels.api as sm

data=pd.read_csv('https://raw.githubusercontent.com/AjStephan/curcumin/main/PubChem_compound_list.csv')

data.head(10)

"""# 2. Clean the data"""

data.info()

"""First we need to see if any data is missing"""

data.isnull().sum()

numerical_data = data.drop(['cmpdname', 'isosmiles'], axis=1)

# Descriptive statistics are very useful for initial exploration of the variables
# By default, only descriptives for the numerical variables are shown
# To include the categorical ones, you should specify this with an argument
numerical_data.describe(include='all')

# Note that categorical variables don't have some types of numerical descriptives
# and numerical variables don't have some types of categorical descriptives

# Let's simply drop all missing values
# This is not always recommended, however, when we remove less than 5% of the data, it is okay

df = numerical_data.dropna(axis=0)

# Let's check the descriptives without the missing values
df.describe(include='all')

"""---"""

df.head()

df.shape

"""#3. Plot correlation matrix"""

df_new = df.drop(['xlogp','exactmass', 'monoisotopicmass'],axis=1)
df_new

# Compute the correlation matrix
correlation_matrix = df_new.corr()

# Create the correlation matrix plot
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix")
plt.show()

import seaborn as sns

sns.heatmap(df_new.corr());

sns.pairplot(df_new);

"""# 4. Run the regression

### Defining the variables and splitting the data
"""

rand_state = 1000

y = df['xlogp']
X = df.drop('xlogp', axis=1) # becareful inplace= False

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=rand_state)

"""## Random Forest Regression with Sklearn"""

from sklearn.ensemble import RandomForestRegressor

# Fitting RF regression to the Training set
RF_regression = RandomForestRegressor(random_state=rand_state)
RF_regression.fit(X_train, y_train)

# Predicting the Test set results
y_hat = RF_regression.predict(X_test)

predictions = pd.DataFrame({ 'y_test':y_test,'y_hat':y_hat})
predictions.head()

"""# 5. Display the evaluation metrics

---
## Evaluating the model performance on test data
"""

import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import seaborn as sns

# Define the models
model = [
    ('Random Forest', RandomForestRegressor())
]
sns.scatterplot(x=y_test, y=y_hat, alpha=0.6)
sns.lineplot(x=y_test, y=y_test)

mse = mean_squared_error(y_test, y_hat)
mae = mean_absolute_error(y_test, y_hat)
r2 = r2_score(y_test, y_hat)
explained_variance = explained_variance_score(y_test, y_hat)


print(f'Mean Squared Error (MSE): {mse}')
print(f'Mean Absolute Error (MAE): {mae}')
print(f'R-squared (R2) Score: {r2}')
print(f'Explained Variance Score: {explained_variance}')
print()

plt.xlabel('Actual count', fontsize=14)
plt.ylabel('Prediced  count', fontsize=14)
plt.title('Actual vs Predicted  count (test set)', fontsize=17)
plt.show()

#sns.scatterplot(x=y_test, y=y_hat, alpha=0.6)
#sns.lineplot(x=y_test, y=y_test)

#plt.xlabel('Actual price', fontsize=14)
#plt.ylabel('Prediced  price', fontsize=14)
#plt.title('Actual vs Predicted  price (test set)', fontsize=17)
#plt.show()

np.round(RF_regression.score(X_test, y_test),4)

MSE_test = round(np.mean(np.square(y_test - y_hat)),2)
MSE_test

MSE_test = round(np.mean(np.square(y_test - y_hat)),2)
RMSE_test = round(np.sqrt(MSE_test),2)
RMSE_test

"""---

#6. Tuning hyperparameters:
### Gridsearch
"""

my_param_grid = {'n_estimators': [10,100,500], 'max_features':['sqrt','log2'], 'max_depth':[5,10,20]}

from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(estimator=RandomForestRegressor(random_state=rand_state),param_grid= my_param_grid, refit = True, verbose=2, cv=5 )
# verbose just means the text output describing the process. (the greater the number the more detail you will get).

# May take a while!
grid.fit(X_train,y_train)

grid.best_params_

grid.best_estimator_

y_hat_optimized = grid.predict(X_test)

predictions['y_hat_optimized'] = y_hat_optimized
predictions.head()

# Define the models
models = [
    ('Random Forest', RandomForestRegressor())
]

sns.scatterplot(x=y_test, y=y_hat_optimized, alpha=0.6)
sns.lineplot(x=y_test, y=y_test)

# Menghitung metrik evaluasi
mse = mean_squared_error(y_test, y_hat)
mae = mean_absolute_error(y_test, y_hat)
r2 = r2_score(y_test, y_hat)
explained_variance = explained_variance_score(y_test, y_hat)

# Menampilkan hasil metrik evaluasi
print(f'Mean Squared Error (MSE): {mse}')
print(f'Mean Absolute Error (MAE): {mae}')
print(f'R-squared (R2) Score: {r2}')
print(f'Explained Variance Score: {explained_variance}')
print()

plt.xlabel('Actual count', fontsize=14)
plt.ylabel('Prediced  count', fontsize=14)
plt.title('Actual vs Predicted  count (test set)', fontsize=17)
plt.show()

#sns.scatterplot(x=y_test, y=y_hat_optimized, alpha=0.6)
#sns.lineplot(x=y_test, y=y_test)

#plt.xlabel('Actual price', fontsize=14)
#plt.ylabel('Prediced  price', fontsize=14)
#plt.title('Actual vs optimized predicted price (test set)', fontsize=17)
#plt.show()

np.round(grid.score(X_test, y_test),4)

MSE_test_opt = round(np.mean(np.square(y_test - y_hat_optimized)),2)
MSE_test_opt

MSE_test_opt = round(np.mean(np.square(y_test - y_hat_optimized)),2)
RMSE_test_opt = round(np.sqrt(MSE_test_opt),2)
RMSE_test_opt

"""#### Cross validation
We will use Cross validation to estimate performance metrics in the test set.
"""

from sklearn.model_selection import cross_val_score

R2 = cross_val_score(estimator = RandomForestRegressor(max_depth=20, max_features='sqrt', n_estimators=500), X = X_train, y = y_train, cv = 5 , scoring="r2" )

R2_CV = round(np.mean(R2),4)
R2_CV

"""---

#7. Feature selection

---

### Feature Importance
"""

features = list(X_train.columns)
features

RF_Regressor = RandomForestRegressor(n_estimators = 500, max_features='sqrt', max_depth=20, random_state= rand_state)
RF_Regressor.fit(X_train, y_train)

importance = RF_Regressor.feature_importances_
importance

FIM = pd.DataFrame({'Features': X_train.columns , 'Feature_importance':importance})
FIM = FIM.sort_values(by=['Feature_importance'])
FIM

plt.figure(figsize=(10,6))
plt.title('Feature Importance')
sns.barplot(y='Features', x='Feature_importance', data=FIM)
plt.show()

"""## Random Forest Regression with Sklearn - NEW"""

df.shape

df_FI = df.drop(['monoisotopicmass', 'mw','hbonddonor','hbondacc','polararea'], axis = 1)

df_FI

y_new = df_FI['xlogp']
X_new = df_FI.drop('xlogp', axis = 1)# becareful inplace= False

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_new, y_new, test_size=0.3, random_state=rand_state)

from sklearn.ensemble import RandomForestRegressor

# Fitting RF regression to the Training set
RF_regression = RandomForestRegressor(random_state=rand_state)
RF_regression.fit(X_train, y_train)

# Predicting the Test set results
y_hat = RF_regression.predict(X_test)

predictions = pd.DataFrame({ 'y_test':y_test,'y_hat':y_hat})
predictions.head()

import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Define the models
model = [
    ('Random Forest', RandomForestRegressor())
]
sns.scatterplot(x=y_test, y=y_hat, alpha=0.6)
sns.lineplot(x=y_test, y=y_test)

# Calculating evaluation metrics
mse = mean_squared_error(y_test, y_hat)
mae = mean_absolute_error(y_test, y_hat)
r2 = r2_score(y_test, y_hat)
explained_variance = explained_variance_score(y_test, y_hat)

# Displaying evaluation metric results
print(f'Mean Squared Error (MSE): {mse}')
print(f'Mean Absolute Error (MAE): {mae}')
print(f'R-squared (R2) Score: {r2}')
print(f'Explained Variance Score: {explained_variance}')
print()

plt.xlabel('Actual count', fontsize=14)
plt.ylabel('Prediced  count', fontsize=14)
plt.title('Actual vs Predicted  count (test set)', fontsize=17)
plt.show()

"""---
---

## Does more important feature mean more significant?
"""

import statsmodels.api as sm

# With statsmodels, we need to mannually add a constant to our dataset!
X_test_wc = sm.add_constant(X_test)
X_train_wc = sm.add_constant(X_train)

# Fit the model
model = sm.OLS(y_train,X_train_wc)
statsmodels_reg= model.fit()

statsmodels_reg.summary()

"""---

###  Additional links:

1. Decision Trees with sklearn: https://scikit-learn.org/stable/modules/tree.html
2. Ensemble learning with sklearn: https://scikit-learn.org/stable/modules/ensemble.html
3. graphviz: this is used for Tree visualization: http://graphviz.org/
4. Out of Bag errors for random forest: https://scikit-learn.org/stable/auto_examples/ensemble/plot_ensemble_oob.html#sphx-glr-auto-examples-ensemble-plot-ensemble-oob-py
"""