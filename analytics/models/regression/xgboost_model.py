import pandas as pd
import numpy as np
import xgboost
from sklearn.model_selection import train_test_split
import data.DataParser as dp
from sklearn.externals import joblib

df = dp.generate_dataset(["Mathematics"])

target = df["Mathematics_9"]
train = df.loc[:, df.columns != 'Mathematics_9']

xgb = xgboost.XGBRegressor(n_estimators=200,learning_rate=0.05) #, gamma=10, subsample=0.75, colsample_bytree=1, max_depth=10
xgb.fit(train, target)

joblib.dump(xgb, 'xgb.joblib') 

clf = joblib.load('xgb.joblib')
