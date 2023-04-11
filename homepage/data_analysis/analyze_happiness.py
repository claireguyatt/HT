# library imports
import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt

class Happiness_Analyzer: 
    
    # data is user data in form of pandas dataframe
    def __init__(self, data):
        self.data = data
    
    # conduct time series multivariate linear regression
    def linear_reg(self):

        # all variables are IDs except happiness
        X = self.data.drop(['Happiness'], axis=1)
        # happiness is DV
        y = self.data['Happiness']

        # create & fit model
        # ***need to add normalizer
        # ***need to make categorical data numerical
        regr = linear_model.LinearRegression()
        regr.fit(X, y)
        print(regr)
