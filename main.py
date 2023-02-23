import pandas as pd
import os
import data_preprocess
import math
from sklearn import linear_model, metrics
import math
from sklearn.metrics import mean_squared_error
from configparser import ConfigParser
import config_file_creation

def main_prog():
    config_file_name = config_file_creation.create_config_file()
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(config_file_name)

    config_param = config_object["data"]
    folder_to_read = "C:/Users/sengupta/Downloads/erizt_data"
    folder_to_write = "C:/Users/sengupta/Downloads/erizt_data_generated"
    files_to_read = list(os.listdir(folder_to_read))
    file = files_to_read[2]
    file = folder_to_read + "/" + file
    data = pd.read_csv(file)
    data = data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]

    data_preprocess_obj = data_preprocess.DataPreprocess(data, int(config_param["time_in_middle"]))
    valid_col = data_preprocess_obj.col_details()
    data = data[valid_col]

    start, end = data_preprocess_obj.start_end()
    start_index = max(start,default=0)
    end_index = min(end, default=-1)

    final_data = data[start_index:end_index]




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_prog()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
