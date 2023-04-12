import numpy as np
import math

class DataColab(object):
    '''
    This class helps in colaboration of data and filling the missing gaps with data
    '''

    def __init__(self, data_act, fwd_data, fwd_index, rev_data, rev_index, config_file):
        self.data_act = data_act
        self.fwd_data = fwd_data
        self.fwd_index = fwd_index
        self.rev_data = rev_data
        self.rev_index = rev_index
        self.config_file = config_file


    def colab(self,c):
        '''
        Here, the missing places are filled up with data. The data can be from either the forward linear regression
        or it can be from the backward linear regression, or it can be from the median if the value is beyond the threshold
        of the attribute in question.
        In case multiple positions are found, then the average of those values are considered.
        :return:
        '''
        start_index = self.data_act.index[0]
        end_index = self.data_act.index[-1]
        if c in ['T1 (°C)', 'T2 (°C)']:
            c = c[:2]
        threshold = self.config_file['threshold_dict'][c]
        max_data = self.data_act.max()*(1+threshold)
        min_data = self.data_act.min()*(1-threshold)
        median_data = self.data_act.median()
        for val_i, i in enumerate(self.fwd_index):
            for val_j, j in enumerate(i):
                if j <= end_index and j >= start_index:
                    if math.isnan(self.data_act[j]):
                        if self.fwd_data[val_i][val_j] > min_data and self.fwd_data[val_i][val_j] < max_data:
                            self.data_act[j] = self.fwd_data[val_i][val_j]
                        else:
                            self.data_act[j] = median_data
                    else:
                        self.data_act[j] = (self.fwd_data[val_i][val_j] + self.data_act[j])/2

        for val_i, i in enumerate(self.rev_index):
            for val_j, j in enumerate(i):
                if j <= end_index and j >= start_index:
                    if math.isnan(self.data_act[j]):
                        if self.rev_data[val_i][val_j] > min_data and self.rev_data[val_i][val_j] < max_data:
                            self.data_act[j] = self.rev_data[val_i][val_j]
                        else:
                            self.data_act[j] = median_data
                    else:
                        self.data_act[j] = (self.rev_data[val_i][val_j] + self.data_act[j])/2
        return self.data_act
