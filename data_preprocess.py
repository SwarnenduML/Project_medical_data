import math
import numpy as np
from configparser import ConfigParser

class DataPreprocess(object):
    '''
    This is where all the preprocessing of the data would happen
    '''
    def __init__(self, data, config_object):
        self.data = data
        self.time_in_middle = int(config_object["data"]["time_in_middle"])
        self.time_trail_preceed = float(config_object["data"]["time_trail_preceed"])

    def count_dups(self,nums):
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
                    if dups[i] <= self.time_in_middle:
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
            if math.isnan(elem[0]) and dups[0]/data.shape[0] < self.time_trail_preceed:
                start_index.append(dups[0])
            elif math.isnan(elem[0]):
                print("Too much NULLs in the front for column "+ c)
                start_index.append(data.shape[0])
            else:
                start_index.append(0)
            if math.isnan(elem[-1]) and dups[0]/data.shape[0] < self.time_trail_preceed:
                end_index.append(dups[-1])
            elif math.isnan(elem[-1]):
                print("Too much NULLs at the back for column " + c)
                end_index.append(-1)
            else:
                end_index.append(data.shape[0])
        return start_index, end_index



