import pandas as pd
import numpy as np
class ML_data_creation():
    def prog_start(self, file_to_operate, config_object):
        master_data = pd.DataFrame([])
        for x in file_to_operate:
            filename = x[x.rfind('/')+1:-4]
            ev_data = pd.read_csv(config_object['folder_for_event_output']+"/"+filename+"_event.csv", index_col = [0])
            data = pd.read_csv(x, index_col = [0])
            if sorted(data.columns) == sorted(['HR (bpm)', 'T1 (°C)','SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']):
                data_needed = data
            else:
                data_needed = data[['HR (bpm)', 'T1 (°C)','SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]
            #data['class_determined']= np.nan
            tmp_var = ev_data.isnull()
            tmp_var_1 = tmp_var.eq(tmp_var.iloc[:,0], axis = 0).all(1)
            ev_data['class'] = np.where(tmp_var_1, 0, 1)
            data_needed['class'] = data_needed.apply(lambda row: self.normalise_row(row), axis=1)
            sum_class  = ev_data['class'] + data_needed['class']
            sum_class_final = np.where(sum_class > 1, 2, sum_class)
#            if (sum_class>1).any():
#                print("class more than 1")
            data['class'] = sum_class_final
            if master_data.shape==(0,0):
                master_data = data
            else:
                master_data = pd.concat([master_data, data], ignore_index = True)
#                print(master_data.shape)
#                print(data.shape)
        return master_data

            #data['class_determined'] = np.where(data['Currency'] == '$', df['Budget'] * 0.78125, df['Budget'])

    def normalise_row(self, row):
        if row.isnull().sum()>0:
            return 2
        else:
            return 0

