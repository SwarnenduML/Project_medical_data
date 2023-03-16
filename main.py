import pandas as pd
import warnings
import data_statistics
warnings.filterwarnings("ignore")
from configparser import ConfigParser

import config_file_creation
import new_data_generation
import data_visual

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
        compiled_data = data_stat_obj.get_statistics()
    if data_visualize =="True":
        if data_stat !="True":
            compiled_data = pd.read_csv(config_object["data"]["folder_to_write"] + "/total_summary_of_data.csv",
                                        index_col=0)
        data_visual_obj = data_visual.DataVisual(compiled_data, config_object)
        data_visual_obj.tot_nulls_per() # Percentage of non-nulls per column per file
        data_visual_obj.log_tot_nulls_per()
        data_visual_obj.non_null_per_file() # Percentage of nulls per file
        data_visual_obj.create_comp() # Compare the input and output file
        data_visual_obj.number_of_col_used()
        data_visual_obj.column_type()






if __name__ == '__main__':
    main_prog()
