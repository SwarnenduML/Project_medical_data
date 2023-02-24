import os
import numpy as np
import pandas as pd
import time

import data_preprocess

class DataStatistics(object):
    '''

    '''
    def __init__(self, config_module):
        self.config_module = config_module

    def get_statistics(self):
        '''

        :return:
        '''
        config_param = self.config_module["data"]
        folder_to_read = config_param["folder_to_read"]
        folder_to_write = config_param["folder_to_write"]
        files_to_read = list(os.listdir(folder_to_read))
        each_file_summary_gen = pd.DataFrame(
            columns=['filename', 'valid_cols', 'start', 'end', 'nulls', 'non_nulls', 'percentage nulls', 'reason'])
        for i,file_to_read in enumerate(files_to_read):
            start_time = time.time()
            print(file_to_read)
            data = pd.read_csv(folder_to_read + "/" + file_to_read)
            data = data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]
            data_preprocess_obj = data_preprocess.DataPreprocess(data, self.config_module)
            valid_col = data_preprocess_obj.col_details()
            start,end = data_preprocess_obj.start_end()
            tmp_df_file = pd.DataFrame(columns=['filename', 'valid_cols', 'start','end','nulls', 'non_nulls', 'percentage nulls','reason'])
            for c in valid_col:
                null_before = data[c].isnull().sum()
                values_present = data[c].count()
                if data.shape[0] == start[valid_col.index(c)]:
                    reason = "too many nulls at start"
                elif -1 == end[valid_col.index(c)]:
                    reason = "too many nulls at end"
                else:
                    reason = ""
                tmp_df_each_col = pd.DataFrame([[file_to_read, c, start[valid_col.index(c)] , end[valid_col.index(c)],
                                                 null_before, values_present, null_before / (null_before + values_present) * 100,reason]],
                                               columns=['filename', 'valid_cols', 'start','end','nulls', 'non_nulls', 'percentage nulls','reason'])
                tmp_df_file = tmp_df_file.append(tmp_df_each_col, ignore_index=True)
            each_file_summary_gen = each_file_summary_gen.append(tmp_df_file, ignore_index=True)

            print(time.time() - start_time)

        print("all done")
        each_file_summary_gen.to_csv(folder_to_write+"/"+"total_summary_of_data.csv")
        return each_file_summary_gen
