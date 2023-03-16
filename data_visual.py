import pandas as pd
import seaborn as sns
import numpy as np
from data_preprocess import DataPreprocess
import matplotlib.pyplot as plt

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
        fig.set_size_inches((12.8,7.2))
        fig.savefig("tot_non_nulls.png")
        fig.clf()

    def log_tot_nulls_per(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.compiled_data[self.compiled_data['reason']!='not a valid column. too many missing values']
        hist_plot = sns.lineplot(data= np.log(data_plot[['percentage non-nulls before', 'percentage non-nulls after']])).set_title("Percentage of non-nulls per column per file")
        fig = hist_plot.get_figure()
        fig.set_size_inches((12.8,7.2))
        fig.savefig("log_tot_non_nulls.png")
        fig.clf()


    def non_null_per_file(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.compiled_data[self.compiled_data['reason'] != 'not a valid column. too many missing values']
        data_plot = data_plot.groupby(['filename']).mean()
        hist_plot = sns.histplot(data=data_plot[['percentage non-nulls before', 'percentage non-nulls after']], element='step',
                                 binwidth=2).set_title("Percentage of non-nulls per file")
        fig = hist_plot.get_figure()
        fig.set_size_inches((12.8,7.2))
        fig.savefig("per_non_nulls_file.png")
        fig.clf()

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
        merged_df = input_data.merge(output_data, how = "left", on = 'index')
        for c in output_data.columns[1:]:
            sns.set_theme()
            line_plot = sns.lineplot(data = merged_df[[c+'_i',c]])
            fig = line_plot.get_figure()
            fig.set_size_inches((12.8, 7.2))
            fig.savefig('comparision_on_'+c+'.png')
            fig.clf()
        print("done")
        #fig.clf()

    def number_of_col_used(self):
        '''

        :return:
        '''
        compiled_data = self.compiled_data[self.compiled_data['reason'] != 'not a valid column. too many missing values']
        comp_data = compiled_data.groupby('filename').count()['valid_cols']
        comp_data.index = range(len(comp_data))
        filenames = list(compiled_data.groupby('filename').count().index)
        no_missing_files = len(list(set(list(self.compiled_data['filename'])) ^ set(filenames)))
        comp_data = comp_data.append(pd.Series([0]*no_missing_files))
        comp_data = comp_data.reset_index(drop=True)
        sns.set_theme()
        hist_plot = sns.histplot(comp_data,bins=6)
        hist_plot.set_xlabel('Number of valid columns per file')
        hist_plot.set_ylabel('Number of files')
        hist_plot.set(title = 'Count of files with valid columns')
        fig = hist_plot.get_figure()
        fig.set_size_inches((12.8,7.2))
        fig.savefig('no_file_valid_col.png')
        fig.clf()

    def column_type(self):
        '''

        :return:
        '''
        compiled_data = self.compiled_data[
            self.compiled_data['reason'] != 'not a valid column. too many missing values']
        comp_data = compiled_data.groupby('valid_cols').count()
        comp_data['valid_cols'] = comp_data.index
        sns.set_theme()
        hist_plot = sns.histplot(comp_data[['valid_cols','filename']],bins=6)
        hist_plot.set_xlabel('Attribute')
        hist_plot.set_ylabel('Number of files')
        hist_plot.set(title = 'Count of files with type columns')
        fig = hist_plot.get_figure()
        fig.set_size_inches((12.8,7.2))
        fig.savefig('type_col_file.png')
        fig.clf()








