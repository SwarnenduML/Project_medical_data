import numpy as np
import math

class DataColab(object):
    '''

    '''

    def __init__(self, data_act, fwd_data, fwd_index, rev_data, rev_index, config_file):
        self.data_act = data_act
        self.fwd_data = fwd_data
        self.fwd_index = fwd_index
        self.rev_data = rev_data
        self.rev_index = rev_index
        self.threshold = float(config_file["data"]["threshold"])

    def colab(self):
        '''

        :return:
        '''
        start_index = self.data_act.index[0]
        end_index = self.data_act.index[-1]
        for val_i, i in enumerate(self.fwd_index):
            for val_j, j in enumerate(i):
                if j < end_index-val_i and j > start_index-val_i:
                    if (math.isnan(self.data_act.iloc[j-1-(start_index-val_i)])) & (self.fwd_data[val_i][val_j] > (1-self.threshold)*self.data_act.min()) \
                        & (self.fwd_data[val_i][val_j] < (1+self.threshold)* self.data_act.max()):
                        self.data_act[j] = self.fwd_data[val_i][val_j]
                    elif math.isnan(self.data_act.iloc[j-1-(start_index+val_i)]):
                        self.data_act.iloc[j-1-(start_index+val_i)] = self.data_act.median()
                    else:
                        self.data_act.iloc[j - 1 - (start_index + val_i)] = (self.data_act.iloc[j - 1 - (start_index + val_i)]+self.fwd_data[val_i][val_j])/2


        for val_i, i in enumerate(self.rev_index):
            for val_j, j in enumerate(i):
                if j < end_index+val_i and j > start_index+val_i:
                    if (math.isnan(self.data_act.iloc[j-1-(start_index+val_i)]) & (self.rev_data[val_i][val_j] > (1-self.threshold)*self.data_act.min()) & (self.rev_data[val_i][val_j] < (1+self.threshold)* self.data_act.max())):
                        self.data_act.iloc[j-1-(start_index+val_i)] = self.rev_data[val_i][val_j]
                    elif math.isnan(self.data_act.iloc[j-1-(start_index+val_i)]):
                        self.data_act.iloc[j-1-(start_index+val_i)] = self.data_act.median()
                    else:
                        self.data_act.iloc[j - 1 - (start_index + val_i)] = (self.data_act.iloc[j - 1 - (start_index + val_i)]+self.rev_data[val_i][val_j])/2
        return self.data_act
