import math
import numpy as np
from configparser import ConfigParser

class DataPreprocess(object):
    '''
    This is where all the preprocessing of the data would happen
    '''
    def __init__(self, data, config_object):
        self.data = data
        self.samples_missed = int(config_object["samples_missed"])
        self.per_data_mis_init = float(config_object['per_data_mis_init'])
        self.per_data_mis_end = float(config_object['per_data_mis_end'])
        assert self.per_data_mis_init > 0
        assert self.per_data_mis_init < 0.5
        assert self.per_data_mis_end > 0
        assert self.per_data_mis_end < 0.5

    def count_dups(self,nums):
        '''
        Here, the number of duplicates are counted. The consecutive NULLs and same values are counted.
        Eg nums - 1,1,2,3,2,1,1,2,2,1 ->  element,freque - 1,2,3,2,1,2,1 ; 2,1,1,1,2,2,1
        :param nums: data in which the running count of duplicates are to be counted
        :return: The return will be the element sequence and their corresponding running frequencies
        '''
        element = []
        freque = []
        running_count = 1
        for i in range(len(nums)-1):
            if nums[i] == nums[i+1] or (math.isnan(nums[i]) and math.isnan(nums[i+1])):
                running_count += 1
            else:
                freque.append(running_count)
                element.append(nums[i])
                running_count = 1
        freque.append(running_count)
        element.append(nums[i+1])
        return element,freque

    def col_details(self):
        '''
        This function tells us if the column is a valid column or not. A valid column is a column if the number of
        consecutive NULLs is less than the number of samples missed as specified in the yaml file.
        :return:
        '''
        df = self.data
        valid_col = []
        for col in df.columns:
            elem, dups = self.count_dups(df[col])
            if math.isnan(elem[0]):
                elem = elem[1:]
                dups = dups[1:]
            if np.isnan(elem).any():
                x = [i for i, x in enumerate(elem) if np.isnan(x)]
                for i in x:
                    if dups[i] <= self.samples_missed:
                        pos = 1
                    else:
                        pos = 0
                        break
                if pos == 1:
                    valid_col.append(col)
            elif len(elem) > 0:
                valid_col.append(col)

        return valid_col

    def start_end(self):
        '''
        This function would determine the starting points and the ending points in the valid columns
        :return: The start and end points of the data
        '''
        valid_col = self.col_details()
        data = self.data[valid_col]
        start_index = []
        end_index = []
        for c in data.columns:
            elem, dups = self.count_dups(data[c])
            if math.isnan(elem[0]) and dups[0]/data.shape[0] < self.per_data_mis_init:
                start_index.append(dups[0])
            elif math.isnan(elem[0]):
                print("Too much NULLs in the front for column "+ c)
                start_index.append(data.shape[0])
            else:
                start_index.append(0)
            if math.isnan(elem[-1]) and dups[0]/data.shape[0] < self.per_data_mis_end:
                end_index.append(data.shape[0]-dups[-1]+1)
            elif math.isnan(elem[-1]):
                print("Too much NULLs at the back for column " + c)
                end_index.append(-1)
            else:
                end_index.append(data.shape[0]+1)
        return start_index, end_index

    def start_end_valid_stat(self):
        '''
        This function would determine the starting points and the ending points in the valid columns. This is needed in
        the used in the generation of the statistical file generation.
        :return: The start and end points of the data
        '''
        valid_col = self.col_details()
        start_index = []
        end_index = []
        data = self.data
        for c in data.columns:
            if c not in valid_col:
                start_index.append(data.shape[0])
                end_index.append(-1)
            else:
                elem, dups = self.count_dups(data[c])
                if math.isnan(elem[0]) and dups[0]/data.shape[0] < self.per_data_mis_init:
                    start_index.append(dups[0])
                elif math.isnan(elem[0]):
                    print("Too much NULLs in the front for column "+ c)
                    start_index.append(data.shape[0])
                else:
                    start_index.append(0)
                if math.isnan(elem[-1]) and dups[0]/data.shape[0] < self.per_data_mis_end:
                    end_index.append(dups[-1])
                elif math.isnan(elem[-1]):
                    print("Too much NULLs at the back for column " + c)
                    end_index.append(-1)
                else:
                    end_index.append(data.shape[0])
        return start_index, end_index


