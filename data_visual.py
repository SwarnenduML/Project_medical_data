import pandas as pd
import seaborn as sns
import numpy as np
from data_preprocess import DataPreprocess
class DataVisual(object):
    '''

    '''
    def __init__(self, data, config_obj):
        self.compiled_data = data
        self.config_obj = config_obj

    def tot_nulls_per(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.compiled_data[self.compiled_data['reason']!='not a valid column. too many missing values']
        hist_plot = sns.histplot(data =data_plot[['percentage non-nulls before', 'percentage non-nulls after']], binwidth = 2,element="step").set_title("Percentage of non-nulls per column per file")
        fig = hist_plot.get_figure()
        fig.savefig("tot_non_nulls.png")
        fig.clear()

    def log_tot_nulls_per(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.compiled_data[self.compiled_data['reason']!='not a valid column. too many missing values']
        hist_plot = sns.histplot(data =np.log(data_plot[['percentage non-nulls before', 'percentage non-nulls after']]), binwidth = 2).set_title("Percentage of non-nulls per column per file")
        fig = hist_plot.get_figure()
        fig.savefig("log_tot_non_nulls.png")
        fig.close()


    def non_null_per_file(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.compiled_data[self.compiled_data['reason'] != 'not a valid column. too many missing values']
        data_plot = data_plot.groupby(['filename']).sum()
        data_plot['non-nulls before'] = data_plot['non_nulls_before'] / data_plot.shape[0] * 100
        data_plot['non-nulls before'] = data_plot['percentage non-nulls before'].astype(float).round(2)
        data_plot['non-nulls after'] = data_plot['non_nulls_after'] / data_plot.shape[0] * 100
        data_plot['non-nulls after'] = data_plot['percentage non-nulls after'].astype(float).round(2)
        hist_plot = sns.histplot(data=data_plot[['percentage non-nulls before', 'percentage non-nulls after']],
                                 binwidth=2).set_title("Percentage of non-nulls per file")
        fig = hist_plot.get_figure()
        fig.savefig("tot_non_nulls_file.png")
        fig.close()

    def create_comp(self):
        '''

        :return:
        '''
        input_dir = self.config_obj["data"]["folder_to_read"]+'/'
        output_dir = self.config_obj["data"]["folder_to_write"]+'/'
        input_path_for_visual = self.config_obj["data"]['data_for_visual']
        output_path_for_visual = input_path_for_visual[:-4]+"_generated.csv"
        input_data = pd.read_csv(input_dir+input_path_for_visual)
        output_data = pd.read_csv(output_dir+output_path_for_visual)
        output_data = output_data.rename({'Unnamed: 0': 'index'}, axis = 1)
        input_data["index"] = input_data.index
        input_data = input_data[output_data.columns]
        input_data = input_data.add_suffix("_i")
        input_data = input_data.rename({'index_i': 'index'}, axis = 1)
        merged_df = pd.concat([input_data, output_data], axis = 1, join = "inner")
        # data_preproc = DataPreprocess(input_data, self.config_obj)
        # valid_col = data_preproc.col_details()
        print("done")
        fig.close()




