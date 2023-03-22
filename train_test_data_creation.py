import numpy as np

class TrainTestDSCreation(object):
    '''
    Here we would be creating the training and the test datasets
    '''
    def __init__(self, fwd_dataset, rev_dataset, config_file):
        self.fwd_dataset = fwd_dataset
        self.rev_dataset = rev_dataset
        self.num_shift = int(config_file["shifting"])

    def train_ds(self):
        '''

        :return:
        '''
        train_ds_fwd = []
        train_ds_rev = []
        for i in range(2,self.num_shift+2):
            train_d_fwd = self.fwd_dataset[self.fwd_dataset.columns[:i]].dropna()
            train_ds_fwd.append(train_d_fwd)

        for i in range(2,self.num_shift+2):
            train_d_rev = self.rev_dataset[self.rev_dataset.columns[:i]].dropna()
            train_ds_rev.append(train_d_rev)

        return train_ds_fwd, train_ds_rev

    def test_ds(self):
        '''

        :return:
        '''
        test_ds_fwd = []
        fwd_pred_index = []
        test_ds_rev = []
        prev_pred_index = []
        for i in range(1,self.num_shift+1):
            test_d_fwd = self.fwd_dataset[self.fwd_dataset[self.fwd_dataset.columns[:i]].notnull().all(axis=1) &
                                          self.fwd_dataset[self.fwd_dataset.columns[i]].isna()][self.fwd_dataset.columns[:i]]
            test_ds_fwd.append(test_d_fwd)
            fwd_pred_index.append(test_d_fwd.index + i)


        for i in range(1,self.num_shift+1):
            test_d_rev = self.rev_dataset[self.rev_dataset[self.rev_dataset.columns[:i]].notnull().all(axis=1) &
                                          self.rev_dataset[self.rev_dataset.columns[i]].isna()][self.rev_dataset.columns[:i]]
            test_ds_rev.append(test_d_rev)
            prev_pred_index.append(test_d_rev.index - i)

        return test_ds_fwd, test_ds_rev, fwd_pred_index, prev_pred_index

