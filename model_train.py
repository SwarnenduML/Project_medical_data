import numpy as np
import pandas as pd
import numpy as np
import os
import math
from sklearn import linear_model, metrics
import math
from sklearn.metrics import mean_squared_error

class ModelTrain(object):
    '''

    '''

    def __init__(self, data_train, data_test):
        self.data_train = data_train
        self.data_test = data_test

    def train_pred_ds(self):
        '''

        :return:
        '''
        x_train = self.data_train[self.data_train.columns[:-1]]
        y_train = self.data_train[self.data_train.columns[-1]]
        x_test = self.data_test
        reg_model = linear_model.LinearRegression()
        reg_model.fit(x_train, y_train)
        pred = reg_model.predict(x_test)
        return pred