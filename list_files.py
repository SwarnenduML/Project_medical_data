import os
import pandas as pd
class ListFiles:
    '''
    This program would help find files of different varieties and would list them down
    '''

    def __init__(self, config_object):
        self.folder = config_object["folder_to_write"]
        self.columns = ['HR (bpm)', 'T1 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']
        self.columns.sort()

    def files_with_col(self, col = 'all'):
        files_to_read = list(os.listdir(self.folder))
        file_to_operate = []
        if col !='all':
            if len(col)>1:
                for f in files_to_read:
                    data = pd.read_csv(self.folder + "/" + f)
                    flag = 0
                    for c in col:
                        if c not in data.columns:
                            print(c + " - Not found in " + f)
                            flag = 1
                    if flag ==0:
                        file_to_operate.append(self.folder + "/" + f)
            else:
                for f in files_to_read:
                    data = pd.read_csv(self.folder + "/" + f)
                    if col not in data.columns:
                        print(col + " - Not found in " + f)
                    else:
                        file_to_operate.append(self.folder + "/" + f)

        else:
            for f in files_to_read:
                #print(f)
                if f[-4:]=='.csv':
                    file = self.folder + "/" + f
                    data = pd.read_csv(file)
                    x = list(data.columns[1:])
                    x.sort()
                    if x == self.columns:
                        file_to_operate.append(self.folder + "/" + f)
                        #print(len(file_to_operate))
        return file_to_operate
