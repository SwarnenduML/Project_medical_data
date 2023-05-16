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
        if col !='all':
            for f in files_to_read:
                data = pd.read_csv(self.folder + "/"+f)
                if col not in f.columns:
                    print(col + " - Not found in " + f)
        else:
            for f in files_to_read:
                #print(f)
                file = self.folder + "/" + f
                data = pd.read_csv(file)
                x = list(data.columns[1:])
                if len(x)==5:
                    print(len(x))
                    print(f)
                    print(x)
                    max_col = len(x)

                x.sort()
                if x == self.columns:
                    print(f)
                    for c in self.columns:
                        print("")
