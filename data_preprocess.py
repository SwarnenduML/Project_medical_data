import math
import numpy as np

class DataPreprocess(object):
    '''
    This is where all the preprocessing of the data would happen
    '''
    def __init__(self, data, time_in_middle):
        self.data = data
        self.time_in_middle = time_in_middle

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

    def col_details(self,df):
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