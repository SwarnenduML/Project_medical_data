import seaborn as sns

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
        hist_plot = sns.histplot(x = self.compiled_data['percentage nulls'], binwidth = 2).set_title("Percentage of nulls per column per file")
        fig = hist_plot.get_figure()
        fig.savefig("tot_nulls.png")


