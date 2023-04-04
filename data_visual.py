import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt


class DataVisual(object):
    '''

    '''

    def __init__(self, data, config_obj, valid_data):
        self.compiled_data = data
        self.config_obj = config_obj
        self.folder_to_plot = self.config_obj['folder_to_plot'] + '/'
        self.no_of_files_read = len(list(os.listdir(self.config_obj['folder_to_read'])))
        self.valid_data = valid_data
        if not os.path.exists(self.config_obj['folder_to_plot']):
            os.mkdir(self.config_obj['folder_to_plot'])
            print("Directory not there. Hence creating")

    def tot_nulls_per(self):
        '''

        :return:
        '''
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        sns.set_theme()
        data_plot = self.valid_data
        hist_plot = sns.histplot(data=data_plot[['percentage non-nulls before', 'percentage non-nulls after']],
                                 binwidth=2, element="step").set_title("Percentage of non-nulls per column per file")
        fig = hist_plot.get_figure()
        #        fig.set_size_inches((12.8,7.2))
        fig.savefig(self.folder_to_plot + "tot_non_nulls.png")
        fig.clf()
        plt.close()

    def log_tot_nulls_per(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.valid_data
        hist_plot = sns.histplot(
            data=np.log(data_plot[['percentage non-nulls before', 'percentage non-nulls after']])).set_title(
            "Percentage of non-nulls per column per file")
        fig = hist_plot.get_figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        #        fig.set_size_inches((12.8,7.2))
        fig.savefig(self.folder_to_plot + "log_tot_non_nulls.png")
        fig.clf()
        plt.close()

    def non_null_per_file(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.valid_data
        data_plot = data_plot.groupby(['filename']).mean()
        hist_plot = sns.histplot(data=data_plot[['percentage non-nulls before', 'percentage non-nulls after']],
                                 element='step',
                                 binwidth=2)
        hist_plot.axhline(self.no_of_files_read)
        hist_plot = hist_plot.set_title("Percentage of non-nulls per file")
        fig = hist_plot.get_figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        #        fig.set_size_inches((12.8,7.2))
        fig.savefig(self.folder_to_plot + "per_non_nulls_file.png")
        fig.clf()
        plt.close()

    def create_comp(self):
        '''

        :return:
        '''
        input_dir = self.config_obj["folder_to_read"] + '/'
        output_dir = self.config_obj["folder_to_write"] + '/'
        input_path_for_visual = self.config_obj['data_for_visual']
        output_path_for_visual = input_path_for_visual[:-4] + "_generated.csv"
        input_data = pd.read_csv(input_dir + input_path_for_visual)
        output_data = pd.read_csv(output_dir + output_path_for_visual)
        output_data = output_data.rename({'Unnamed: 0': 'index'}, axis=1)
        input_data["index"] = input_data.index
        input_data = input_data[output_data.columns]
        input_data = input_data.add_suffix("_i")
        input_data = input_data.rename({'index_i': 'index'}, axis=1)
        merged_df = input_data.merge(output_data, how="left", on='index')
        for c in output_data.columns[1:]:
            fig, axes = plt.subplots(1, 2, sharey=True)
            line_plot = sns.lineplot(ax=axes[0], data=merged_df[c + '_i'])
            axes[0].set(title=input_path_for_visual, xlabel='index', ylabel='value')
            line_plot = sns.lineplot(ax=axes[1], data=merged_df[c])
            axes[1].set(title=input_path_for_visual, xlabel='index', ylabel='value')
            fig = line_plot.get_figure()
            #           fig.set_size_inches((12.8, 7.2))
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
            fig.savefig(self.folder_to_plot + 'comparision_on_' + c + '.png')
            fig.clf()
        print("done")
        plt.close()
        # fig.clf()

    def number_of_col_used(self):
        '''

        :return:
        '''
        compiled_data = self.valid_data
        comp_data = compiled_data.groupby(['filename'])['valid_cols'].apply(','.join).reset_index()['valid_cols']
        sns.set_theme()
        hist_plot = sns.histplot(comp_data, bins=6)
        hist_plot.axhline(self.no_of_files_read)
        hist_plot.set_xticklabels(hist_plot.get_xticklabels(), rotation=45, horizontalalignment='right',
                                  fontweight='light', fontsize='smaller')
        hist_plot.set_xlabel('Number of valid columns per file')
        hist_plot.set_ylabel('Number of files')
        hist_plot.set(title='Count of files with valid columns')
        fig = hist_plot.get_figure()
        #        fig.set_size_inches((12.8,7.2))
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        fig.savefig(self.folder_to_plot + 'no_file_valid_col.jpg')
        fig.clf()
        plt.close()
        print(comp_data.value_counts())

    def column_type(self):
        '''

        :return:
        '''
        compiled_data = self.valid_data
        comp_data = compiled_data.groupby('valid_cols').count()
        comp_data['valid_cols'] = comp_data.index
        sns.set_theme()
        bar_plot = sns.barplot(data=comp_data, y='filename', x='valid_cols')
        bar_plot.axhline(self.no_of_files_read)
        bar_plot.set_xlabel('Attribute')
        bar_plot.set_ylabel('Number of files')
        bar_plot.set(title='Count of files with type columns')
        fig = bar_plot.get_figure()
        #        fig.set_size_inches((12.8,7.2))
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        fig.savefig(self.folder_to_plot + 'type_col_file.png')
        fig.clf()
        plt.close()

    def visual_best_diff(self):
        '''

        :return:
        '''
        compiled_data = self.valid_data
        comp_data = compiled_data.groupby('filename').count()['valid_cols']
        file_max_val_col = compiled_data[
            compiled_data['filename'].isin(list(comp_data[comp_data == comp_data.max()].index))]
        file_max_per = list(file_max_val_col[file_max_val_col['diff non null percentage'] == file_max_val_col[
            'diff non null percentage'].max()]['filename'])[0]
        file_max_no = list(
            file_max_val_col[file_max_val_col['diff non nulls'] == file_max_val_col['diff non nulls'].max()][
                'filename'])[0]
        print('Best in number: ' + file_max_no)
        print('Best in percentage: ' + file_max_per)
        self.create_comp_file(file_max_no)
        self.create_comp_file(file_max_per)
        plt.close()

    def create_comp_file(self, file):
        '''

        :return:
        '''
        input_dir = self.config_obj["folder_to_read"] + '/'
        output_dir = self.config_obj["folder_to_write"] + '/'
        input_path_for_visual = file
        output_path_for_visual = input_path_for_visual[:-4] + "_generated.csv"
        input_data = pd.read_csv(input_dir + input_path_for_visual)
        output_data = pd.read_csv(output_dir + output_path_for_visual)
        output_data = output_data.rename({'Unnamed: 0': 'index'}, axis=1)
        input_data["index"] = input_data.index
        input_data = input_data[output_data.columns]
        input_data = input_data.add_suffix("_i")
        input_data = input_data.rename({'index_i': 'index'}, axis=1)
        merged_df = input_data.merge(output_data, how="left", on='index')
        for c in output_data.columns[1:]:
            fig, axes = plt.subplots(1, 2, sharey=True)
            line_plot = sns.lineplot(ax=axes[0], data=merged_df[c + '_i'])
            axes[0].set(title=input_path_for_visual, xlabel='index', ylabel='value')
            line_plot = sns.lineplot(ax=axes[1], data=merged_df[c])
            axes[1].set(title=input_path_for_visual, xlabel='index', ylabel='value')
            fig = line_plot.get_figure()
            #            fig.set_size_inches((12.8, 7.2))
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
            fig.savefig(self.folder_to_plot + 'comparision_on_' + c + '.png')
            fig.clf()
        print("done")
        plt.close()

    def create_comp_file_col(self, file, col):
        '''

        :return:
        '''
        input_dir = self.config_obj["folder_to_read"] + '/'
        output_dir = self.config_obj["folder_to_write"] + '/'
        input_path_for_visual = file
        output_path_for_visual = input_path_for_visual[:-4] + "_generated.csv"
        input_data = pd.read_csv(input_dir + input_path_for_visual)
        output_data = pd.read_csv(output_dir + output_path_for_visual)
        output_data = output_data.rename({'Unnamed: 0': 'index'}, axis=1)
        input_data["index"] = input_data.index
        input_data = input_data[output_data.columns]
        input_data = input_data.add_suffix("_i")
        input_data = input_data.rename({'index_i': 'index'}, axis=1)
        merged_df = input_data.merge(output_data, how="left", on='index')
        sns.set_theme()
        if col in output_data.columns:
            line_plot = sns.lineplot(data=merged_df[[col + '_i', col]])
            line_plot.set(title=file, xlabel='index', ylabel='value')
            fig = line_plot.get_figure()
            #            fig.set_size_inches((12.8, 7.2))
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
            fig.savefig(self.folder_to_plot + 'max_diff_comp_' + col + '_' + file[:-4] + '.png')
            fig.clf()
        else:
            print(col + ' not found')
        print("done")
        plt.close()

    def data_retention_per(self):
        compiled_data = self.valid_data
        compiled_data = compiled_data.groupby('filename').mean()
        compiled_data.reset_index(inplace=True, drop=True)
        sns.set_theme()
        hist_plot = sns.histplot(data=compiled_data['data retention'], binwidth=0.5, element="step")
        hist_plot.set_xlabel('Number')
        hist_plot.set_ylabel('Percentage of data retention')
        hist_plot.set(title='Total percentage of data retention per file')
        hist_plot.axhline(compiled_data.shape[0])
        fig = hist_plot.get_figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        fig.savefig(self.folder_to_plot + 'val_data_retention.png')
        fig.clf()
        plt.close()

    def data_gen_per(self):
        compiled_data = self.valid_data
        compiled_data = compiled_data.groupby('filename').mean()
        compiled_data.reset_index(inplace=True, drop=True)
        sns.set_theme()
        hist_plot = sns.histplot(data=compiled_data['data generation'], binwidth=0.5, element="step")
        hist_plot.set_xlabel('Attributes')
        hist_plot.set_ylabel('Percentage of data generation')
        hist_plot.set(title='Total percentage of data generation per file')
        hist_plot.axhline(compiled_data.shape[0])
        fig = hist_plot.get_figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        fig.savefig(self.folder_to_plot + 'val_data_gen.png')
        fig.clf()
        plt.close()

    def data_retention_per_atr(self):
        compiled_data = self.valid_data
        compiled_data.reset_index(inplace=True, drop=True)
        compiled_data = compiled_data.groupby('valid_cols').mean()
        compiled_data.reset_index(inplace=True)
        sns.set_theme()
        bar_plot = sns.barplot(data=compiled_data, y='data retention', x='valid_cols')
        bar_plot.set_xlabel('Attributes')
        bar_plot.set_ylabel('Percentage of data retention')
        bar_plot.set(title='Total percentage of data retention per attribute')
        fig = bar_plot.get_figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        fig.savefig(self.folder_to_plot + 'val_data_retention_atr.png')
        fig.clf()
        plt.close()

    def data_gen_per_atr(self):
        compiled_data = self.valid_data
        compiled_data.reset_index(inplace=True, drop=True)
        sns.set_theme()
        bar_plot = sns.barplot(data=compiled_data, y='data generation', x='valid_cols')
        bar_plot.set_xlabel('Number')
        bar_plot.set_ylabel('Percentage of data generation')
        bar_plot.set(title='Total percentage of data generation of valid files')
        fig = bar_plot.get_figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        fig.savefig(self.folder_to_plot + 'val_data_gen_atr.png')
        fig.clf()
        plt.close()

    def per_gen_atr(self):
        compiled_data = self.valid_data
        atr = list(compiled_data['valid_cols'].unique())
        for c in atr:
            tmp_list = compiled_data[compiled_data['valid_cols'] == c]
            hist_plot = sns.histplot(data=tmp_list['data generation'], bins=10, element="step")
            hist_plot.set_ylabel('Percentage of data generation')
            hist_plot.set(title='Total percentage of data generation for attribute ' + c)
            fig = hist_plot.get_figure()
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
            fig.savefig(self.folder_to_plot + 'val_data_gen_' + c + '.png')
            fig.clf()
            plt.close()
