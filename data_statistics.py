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
            columns=['filename', 'valid_cols', 'start','end','nulls_before',
                                    'non_nulls_before','nulls_after','non_nulls_after','percentage nulls before',
                                                'percentage nulls after','reason'])
        for i,file_to_read in enumerate(files_to_read):
            start_time = time.time()
            #print(file_to_read)
            input_data = pd.read_csv(folder_to_read + "/" + file_to_read)
            output_data = pd.read_csv(folder_to_write + "/" + file_to_read[:-4]+"_generated.csv")
            input_data = input_data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]
#            output_data = output_data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]
            data_preprocess_obj = data_preprocess.DataPreprocess(input_data, self.config_module)
            start,end = data_preprocess_obj.start_end_valid_stat()
            tmp_df_file = pd.DataFrame(columns=['filename', 'valid_cols', 'start','end','nulls_before',
                                    'non_nulls_before','nulls_after','non_nulls_after','percentage nulls before',
                                                'percentage nulls after','reason'])
            for i,c in enumerate(input_data.columns):
                null_before = input_data[c].isnull().sum()
                values_before = input_data[c].count()
                nulls_after, values_after = 0,0
                if input_data.shape[0] == start[i] and -1 == end[i]:
                    reason = "not a valid column. too many missing values"
                    nulls_after, values_after = 0, -1
                elif input_data.shape[0] == start[i]:
                    reason = "too many nulls at start"
                elif -1 == end[i]:
                    reason = "too many nulls at end"
                else:
                    reason = ""
                    nulls_after = output_data[c].isnull().sum()
                    values_after = output_data[c].count()
                per_nulls_before = float("{:.2f}".format(null_before / (null_before + values_before) * 100))
                per_nulls_after = float("{:.2f}".format(nulls_after / (nulls_after + values_after) * 100))
                tmp_df_each_col = pd.DataFrame([[file_to_read, c, start[i], end[i], null_before, values_before,
                                                 nulls_after, values_after ,per_nulls_before, per_nulls_after,reason]],
                                               columns=['filename', 'valid_cols', 'start', 'end', 'nulls_before',
                                                        'non_nulls_before', 'nulls_after', 'non_nulls_after',
                                                        'percentage nulls before',
                                                        'percentage nulls after', 'reason'])
                tmp_df_file = tmp_df_file.append(tmp_df_each_col, ignore_index=True)
            each_file_summary_gen = each_file_summary_gen.append(tmp_df_file, ignore_index=True)

            #print(time.time() - start_time)

        print("all done")
        each_file_summary_gen.to_csv(folder_to_write+"/"+"total_summary_of_data.csv")
        each_file_summary_gen.to_excel(folder_to_write+"/"+"summary_of_data.xlsx")
        return each_file_summary_gen
