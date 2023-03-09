import seaborn as sns
from matplotlib import pyplot as plt

class DataVisual(object):
    '''

    '''
    def __init__(self, data):
        self.compiled_data = data

    def tot_nulls_per(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.compiled_data[self.compiled_data['reason']!='not a valid column. too many missing values']
        hist_plot = sns.histplot(data =data_plot[['percentage nulls before', 'percentage nulls after']], binwidth = 2).set_title("Percentage of nulls per column per file")
        fig = hist_plot.get_figure()
        fig.savefig("tot_nulls.png")

    def null_per_file(self):
        '''

        :return:
        '''
        sns.set_theme()
        data_plot = self.compiled_data[self.compiled_data['reason'] != 'not a valid column. too many missing values']
        data_plot = data_plot.groupby(['filename']).sum()
        data_plot['percentage nulls before'] = float("{:.2f}".format(data_plot['null_before'] / (data_plot['null_before'] + data_plot['values_before']) * 100))
        data_plot['percentage nulls after'] = float("{:.2f}".format(data_plot['nulls_after'] / (data_plot['nulls_after'] + data_plot['values_after']) * 100))
        hist_plot = sns.histplot(data=data_plot[['percentage nulls before', 'percentage nulls after']],
                                 binwidth=2).set_title("Percentage of nulls per file")
        fig = hist_plot.get_figure()
        fig.savefig("tot_nulls_file.png")


