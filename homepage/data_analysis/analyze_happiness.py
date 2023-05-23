# library imports
import base64
from io import BytesIO
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import OrdinalEncoder
from matplotlib.figure import Figure
from matplotlib import pyplot as plt  
from sklearn.metrics import mean_squared_error, r2_score

class Happiness_Analyzer: 
    
    # data is user data in form of pandas dataframe
    def __init__(self, data):
        self.data = data
        self.X = self.data.drop(['Happiness'], axis=1)
        self.y = self.data['Happiness']
        self.preprocess()
        #self.lin_reg = 
        #self.plot = self.plot()

    def preprocess(self):
        # deal with missing vals

        # deal with categorical data
        # Apply ordinal encoder to each column with categorical data
        ordinal_encoder = OrdinalEncoder()
        self.X = ordinal_encoder.fit_transform(self.X)
    
    # conduct time series multivariate linear regression
    def linear_reg(self):

        # Split the data into training/testing sets
        X_train = self.X[:-10]
        #print("xtrain: ", X_train)
        X_test = self.X[-10:]

        # Split the targets into training/testing sets
        y_train = self.y[:-10]
        #print("ytrain: ", y_train)
        y_test = self.y[-10:]

        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(X_train, y_train)

        # Make predictions using the testing set
        y_pred = regr.predict(X_test)

        # The coefficients
        print("Coefficients: \n", regr.coef_)
        # The mean squared error
        print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
        # The coefficient of determination: 1 is perfect prediction
        print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

        # Generate the figure **without using pyplot**
        fig = Figure()
        ax = fig.subplots()
        sleep_data = self.data['Sleep'].values.tolist()
        hap_data = self.data['Happiness'].values.tolist()
        print(type(self.data['Sleep'].values.tolist()))
        ax.plot(sleep_data, hap_data)
        ax.set_xlabel('Display X-axis Label', 
               fontweight ='bold')

        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        analysis = base64.b64encode(buf.getbuffer()).decode("ascii")
        # return analysis
        return f"<img src='data:image/png;base64,{analysis}'/>"

    def plot(self):

        pass

        # create & fit model
        # ***need to add normalizer





    


