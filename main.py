import pandas as pd
import os
import time
import warnings

import data_statistics

warnings.filterwarnings("ignore")

import data_preprocess
from configparser import ConfigParser
import config_file_creation
import new_data_generation

def main_prog():
    config_file_name = config_file_creation.create_config_file()
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(config_file_name)
    data_gen = config_object["data"]["data_gen"]
    data_stat = config_object["data"]["data_stat"]
    data_visualize = config_object["data"]["data_visualize"]
    if data_gen=="True":
        data_generator_obj = new_data_generation.NewDataGeneration(config_object)
        data_generator_obj.create_data()
    if data_stat =="True":
        data_stat_obj = data_statistics.DataStatistics(config_object)
        data_stat_obj.get_statistics()



if __name__ == '__main__':
    main_prog()
