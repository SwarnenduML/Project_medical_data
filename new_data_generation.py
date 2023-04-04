import pandas as pd
import os
import time
import warnings
warnings.filterwarnings("ignore")

import data_preprocess
from configparser import ConfigParser
import config_file_creation
import data_transform
import train_test_data_creation
import model_train
import data_colab


class NewDataGeneration(object):
    '''
    This class is used when we want to create new modified data
    '''
    def __init__(self, config_module):
        self.config_module = config_module
        if not os.path.exists(self.config_module['folder_to_write']):
            os.mkdir(self.config_module['folder_to_write'])

    def create_data(self):
        '''

        :return:
        '''
        config_param = self.config_module
        folder_to_read = config_param["folder_to_read"]
        folder_to_write = config_param["folder_to_write"]
        files_to_read = list(os.listdir(folder_to_read))
        for file_to_read in files_to_read:
            print(file_to_read)
#            file_to_read = '014-220303-183038.csv'
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

            for i,c in enumerate(final_data.columns):
                counter = 0
#                final_data = data[c][start[i]:end[i]]
                #            print(c)
                while final_data[c].isna().any():
                    if counter > int(self.config_module['samples_missed']):
                        break
                    else:
                        counter = counter+1
                        #               print(final_data[c].isna().sum())
                        fwd_shift_obj = data_transform.DataTransform(final_data[c], self.config_module)
                        fwd_shift_data = fwd_shift_obj.shifting("fwd")
                        rev_shift_obj = data_transform.DataTransform(final_data[c], self.config_module)
                        rev_shift_data = rev_shift_obj.shifting("bck")

                        train_test_ds_creation_obj = train_test_data_creation.TrainTestDSCreation(fwd_shift_data,
                                                                                                   rev_shift_data,
                                                                                                   self.config_module)
                        train_ds_fwd, train_ds_rev = train_test_ds_creation_obj.train_ds()
                        test_ds_fwd, test_ds_rev, pred_index_ds_fwd, pred_index_ds_rev = train_test_ds_creation_obj.test_ds()

                        pred_fwd = []
                        pred_index_fwd = []
                        pred_rev = []
                        pred_index_rev = []
                        for i in range(len(test_ds_fwd)):
                            model = model_train.ModelTrain(train_ds_fwd[i], test_ds_fwd[i])
                            pred = model.train_pred_ds()
                            pred_fwd.append(pred)
                            pred_index_fwd.append(pred_index_ds_fwd[i])

                        for i in range(len(test_ds_rev)):
                            model = model_train.ModelTrain(train_ds_rev[i], test_ds_rev[i])
                            pred = model.train_pred_ds()
                            pred_rev.append(pred)
                            pred_index_rev.append(pred_index_ds_rev[i])

                        data_colab_obj = data_colab.DataColab(final_data[c], pred_fwd, pred_index_fwd, pred_rev,
                                                              pred_index_rev, self.config_module)
                        final_data[c] = data_colab_obj.colab(c)
            print(time.time() - start_time)
            final_data.to_csv(folder_to_write + "/" + file_to_read[:-4] + "_generated.csv")
            if not os.path.exists("C:/Users/sengupta/Downloads/erizt_data_generated_excel/"):
                os.mkdir("C:/Users/sengupta/Downloads/erizt_data_generated_excel/")
            final_data.to_excel("C:/Users/sengupta/Downloads/erizt_data_generated_excel/"+file_to_read[:-4]+"_gen.xlsx")
            if not os.path.exists("C:/Users/sengupta/Downloads/erizt_data_excel/"):
                os.mkdir("C:/Users/sengupta/Downloads/erizt_data_excel/")
            pd.read_csv(folder_to_read+"/"+file_to_read).to_excel("C:/Users/sengupta/Downloads/erizt_data_excel/"+file_to_read[:-3]+"xlsx")
