# library imports
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import OrdinalEncoder
import matplotlib.pyplot as plt

class Happiness_Analyzer: 
    
    # data is user data in form of pandas dataframe
    def __init__(self, data):
        self.data = data
        self.X = self.data.drop(['Happiness'], axis=1)
        self.y = self.data['Happiness']

    def preprocess(self):
        # deal with missing vals

        # deal with categorical data
        # Apply ordinal encoder to each column with categorical data
        ordinal_encoder = OrdinalEncoder()
        self.X = ordinal_encoder.fit_transform(self.X)
    
    # conduct time series multivariate linear regression
    def linear_reg(self):

        # create & fit model
        # ***need to add normalizer
        # ***need to make categorical data numerical
        regr = linear_model.LinearRegression()
        regr.fit(self.X, self.y)
        print(regr)
