import pandas as pd
import numpy as np
from configparser import ConfigParser

class DataTransform(object):
    '''
    This class contains the data transformations like shifting in forward and backward direction, etc
    '''

    def __init__(self, data, config_file):
        self.data = data
        self.config_file = config_file
        self.num_shift = int(self.config_file["shifting"])

    def shifting(self, type):
        '''
        This function generates the shifted version of the dataset such that the linear regression can be done. The type
        can be either forward shift "fwd" or reverse shift "bck"
        :return: Returns the data after the shift is done per column
        '''
        data = pd.DataFrame(self.data)
        data.columns = ["init"]
        if type =="fwd":
            i=1
            while i<=self.num_shift:
                data['init_'+str(i)] = data["init"].shift(-i)
                i=i+1
        elif type =="bck":
            i=1
            while i<=self.num_shift:
                data['init_'+str(i)] = data["init"].shift(i)
                i=i+1
        return data


