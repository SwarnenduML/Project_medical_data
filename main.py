import pandas as pd
import os
import data_preprocess
import math
from sklearn import linear_model, metrics
import math
from sklearn.metrics import mean_squared_error
from configparser import ConfigParser

def main_prog():
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    config_param = config_object["data"]
    folder_to_read = "C:/Users/sengupta/Downloads/erizt_data"
    folder_to_write = "C:/Users/sengupta/Downloads/erizt_data_generated"
    files_to_read = list(os.listdir(folder_to_read))
    file = files_to_read[2]
    file = folder_to_read + "/" + file
    data = pd.read_csv(file)
    data = data[['HR (bpm)', 'T1 (°C)', 'T2 (°C)', 'SPO2 (%)', 'AWRR (rpm)', 'CO2 (mmHg)']]

    valid_col = data_preprocess.DataPreprocess(data, config_param["time_in_middle"])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_prog()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
