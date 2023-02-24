import pandas as pd
import os
import time
import warnings
warnings.filterwarnings("ignore")

import data_preprocess
from configparser import ConfigParser
import config_file_creation
import data_transform
import train__test_data_creation
import model_train
import data_colab


class NewDataGeneration(object):
    '''
    This class is used when we want to create new modified data
    '''
    def __init__(self, config_module):
        self.config_module = config_module

    def create_data(self):
        '''

        :return:
        '''
        config_param = self.config_module["data"]
        folder_to_read = config_param["folder_to_read"]
        folder_to_write = config_param["folder_to_write"]
        files_to_read = list(os.listdir(folder_to_read))
        for file_to_read in files_to_read:
            print(file_to_read)
            file_to_read = "003-210505-103346.csv"
            start_time = time.time()
            file = folder_to_read + "/" + file_to_read
            data = pd.read_csv(file)
            data = data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]

            data_preprocess_obj = data_preprocess.DataPreprocess(data, self.config_module)
            valid_col = data_preprocess_obj.col_details()
            data = data[valid_col]

            start, end = data_preprocess_obj.start_end()
            start_index = max(start, default=0)
            end_index = min(end, default=-1)

            final_data = data[start_index:end_index]

            for c in final_data.columns:
                #            print(c)
                while final_data[c].isna().any():
                    #               print(final_data[c].isna().sum())
                    fwd_shift_obj = data_transform.DataTransform(final_data[c], self.config_module)
                    fwd_shift_data = fwd_shift_obj.shifting("fwd")
                    rev_shift_obj = data_transform.DataTransform(final_data[c], self.config_module)
                    rev_shift_data = rev_shift_obj.shifting("bck")

                    train_test_ds_creation_obj = train__test_data_creation.TrainTestDSCreation(fwd_shift_data,
                                                                                               rev_shift_data,
                                                                                               self.config_module)
                    train_ds_fwd, train_ds_rev = train_test_ds_creation_obj.train_ds()
                    test_ds_fwd, test_ds_rev = train_test_ds_creation_obj.test_ds()

                    pred_fwd = []
                    pred_index_fwd = []
                    pred_rev = []
                    pred_index_rev = []
                    for i in range(len(test_ds_fwd)):
                        model = model_train.ModelTrain(train_ds_fwd[i], test_ds_fwd[i])
                        pred = model.train_pred_ds()
                        pred_fwd.append(pred)
                        pred_index_fwd.append(test_ds_fwd[i].index)

                        model = model_train.ModelTrain(train_ds_rev[i], test_ds_rev[i])
                        pred = model.train_pred_ds()
                        pred_rev.append(pred)
                        pred_index_rev.append(test_ds_rev[i].index)

                    data_colab_obj = data_colab.DataColab(final_data[c], pred_fwd, pred_index_fwd, pred_rev,
                                                          pred_index_rev, self.config_module)
                    final_data[c] = data_colab_obj.colab()
            print(time.time() - start_time)
            final_data.to_csv(folder_to_write + "/" + file_to_read[:-4] + "_generated.csv")
