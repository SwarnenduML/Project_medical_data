import pandas as pd
import os
import time
import warnings
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
    data_gen = config_object["data"][]
    if data_gen:
        data_generator_obj = new_data_generation.NewDataGeneration(config_object)



if __name__ == '__main__':
    main_prog()
