from sklearn import linear_model, metrics

class ModelTrain(object):
    '''
    This class trains the model and returns the prediction output of the dataset for it to be filled into the null value
    '''

    def __init__(self, data_train, data_test):
        self.data_train = data_train
        self.data_test = data_test

    def train_pred_ds(self):
        '''
        This function predicts the values that could be present in the null values
        :return: the predicted values at the null positions
        '''
        x_train = self.data_train[self.data_train.columns[:-1]]
        y_train = self.data_train[self.data_train.columns[-1]]
        x_test = self.data_test
        reg_model = linear_model.LinearRegression()
        reg_model.fit(x_train, y_train)
        pred = reg_model.predict(x_test)
        return pred