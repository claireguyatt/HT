import pandas as pd
import matplotlib.pyplot as plt

class HappinessAnalyzer:

    # constructor, data is a pandas DataFrame
    def __init__(self, data): 
        self.data = data
    
    # check assumptions
    def assumptions_check(self):

        # check for linearity
        plt.scatter(self.data['happiness'], self.data[0], color='red')
        plt.title('Happiness vs Var1', fontsize=14)
        plt.xlabel('Happiness', fontsize=14)
        plt.ylabel('Var1', fontsize=14)
        plt.grid(True)
        plt.show()
    
    # multivariate time series linear regression
