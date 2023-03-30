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
        config_param = self.config_module
        folder_to_read = config_param["folder_to_read"]
        folder_to_write = config_param["folder_to_write"]
        files_to_read = list(os.listdir(folder_to_read))
        each_file_summary_gen = pd.DataFrame(
            columns=['filename', 'valid_cols', 'nulls_before',
                     'non_nulls_before', 'nulls_after', 'non_nulls_after', 'reason'])
        start_time = time.time()
        for i, file_to_read in enumerate(files_to_read):
            #            file_to_read = '002-210510-165039.csv'
            print(file_to_read)
            input_data = pd.read_csv(folder_to_read + "/" + file_to_read)
            output_data = pd.read_csv(folder_to_write + "/" + file_to_read[:-4] + "_generated.csv")
            input_data = input_data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]
            #            output_data = output_data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]
            data_preprocess_obj = data_preprocess.DataPreprocess(input_data, self.config_module)
            start, end = data_preprocess_obj.start_end_valid_stat()
            tmp_df_file = pd.DataFrame(columns=['filename', 'valid_cols', 'nulls_before',
                                                'non_nulls_before', 'nulls_after', 'non_nulls_after',
                                                'percentage non-nulls before',
                                                'percentage non-nulls after', 'diff non nulls',
                                                'diff non null percentage', 'reason'])
            for i, c in enumerate(input_data.columns):
                null_before = input_data[c].isnull().sum()
                values_before = input_data[c].count()
                nulls_after, values_after = 0, 0
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
                per_nonnulls_before = float("{:.2f}".format(values_before / input_data.shape[0] * 100))
                per_nonnulls_after = float("{:.2f}".format(values_after / input_data.shape[0] * 100))
                diff_non_nulls, diff_non_null_per = values_after - values_before, per_nonnulls_after - per_nonnulls_before
                data_generation = values_after - values_before
                if data_generation >= 0:
                    data_retention = 100
                else:
                    data_retention = float("{:.2f}".format((values_before - values_after) * 100 / values_before))
                data_missing_init = float(
                    "{:.2f}".format((input_data.shape[0] - input_data[c].count()) * 100 / input_data.shape[0]))
                if c in output_data.columns:
                    data_missing_final = float(
                        "{:.2f}".format((input_data.shape[0] - output_data[c].count()) * 100 / input_data.shape[0]))
                else:
                    data_missing_final = 100
                tmp_df_each_col = pd.DataFrame([[file_to_read, c, null_before, values_before,
                                                 nulls_after, values_after, per_nonnulls_before, per_nonnulls_after,
                                                 diff_non_nulls, diff_non_null_per, reason,
                                                 data_retention, data_generation, data_missing_init,
                                                 data_missing_final]],
                                               columns=['filename', 'valid_cols', 'nulls_before',
                                                        'non_nulls_before', 'nulls_after', 'non_nulls_after',
                                                        'percentage non-nulls before',
                                                        'percentage non-nulls after', 'diff non nulls',
                                                        'diff non null percentage', 'reason',
                                                        'data retention', 'data generation', 'data missing initial',
                                                        'data missing final'])
                tmp_df_file = tmp_df_file.append(tmp_df_each_col, ignore_index=True)
            each_file_summary_gen = each_file_summary_gen.append(tmp_df_file, ignore_index=True)

        print(time.time() - start_time)

        print("all done")
        each_file_summary_gen.to_csv(folder_to_write + "/" + "total_summary_of_data.csv")
        each_file_summary_gen.to_excel(folder_to_write + "/" + "summary_of_data.xlsx")
        result_df = each_file_summary_gen[each_file_summary_gen['reason'] == ""]
        result_df.drop(columns = 'reason', inplace=True)
        result_df.to_csv(folder_to_write + "/" + "total_summary_of_valid_data.csv")
        result_df.to_excel(folder_to_write + "/" + "summary_of_valid_data.xlsx")
        return each_file_summary_gen
