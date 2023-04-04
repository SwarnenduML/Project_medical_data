import pandas as pd
import warnings
import data_statistics
warnings.filterwarnings("ignore")
import yaml
#from configparser import ConfigParser

import new_data_generation
import data_visual

def main_prog():
    # config_file_name = config_file_creation.create_config_file()
    # Read config.ini file
    with open("req_yaml.yml", 'r') as stream:
        config_object = yaml.safe_load(stream)
    data_gen = config_object["data_gen"]
    data_stat = config_object["data_stat"]
    data_visualize = config_object["data_visualize"]
    if data_gen:
        data_generator_obj = new_data_generation.NewDataGeneration(config_object)
        data_generator_obj.create_data()
    if data_stat:
        data_stat_obj = data_statistics.DataStatistics(config_object)
        compiled_data, valid_data = data_stat_obj.get_statistics()
    if data_visualize:
        if not data_stat:
            compiled_data = pd.read_csv(config_object["folder_to_write"] + "/total_summary_of_data.csv",
                                        index_col=0)
            valid_data = pd.read_csv(config_object["folder_to_write"] + "/total_summary_of_valid_data.csv",
                                        index_col=0)
        data_visual_obj = data_visual.DataVisual(compiled_data,config_object,valid_data)
#        data_visual_obj.tot_nulls_per() # Percentage of non-nulls per column per file
        data_visual_obj.log_tot_nulls_per()
        data_visual_obj.non_null_per_file() # Percentage of nulls per file
        data_visual_obj.create_comp() # Compare the input and output file
        data_visual_obj.number_of_col_used()
        data_visual_obj.column_type()
        data_visual_obj.visual_best_diff()
        col = list(compiled_data.groupby('valid_cols').first().index)
        for c in col:
            comp_d = compiled_data[compiled_data['reason']!='not a valid column. too many missing values']
            comp_d = comp_d[comp_d['valid_cols']==c]
            file_no = list(comp_d[comp_d['diff non nulls']==comp_d['diff non nulls'].max()]['filename'])[0]
            file_per = list(comp_d[comp_d['diff non null percentage'] == comp_d['diff non null percentage'].max()]['filename'])[0]
            print('Best in number for columns '+c+' : ' + file_no)
            print('Best in percentage for columns '+c+' : ' + file_per)
            data_visual_obj.create_comp_file_col(file_no,c)
            data_visual_obj.create_comp_file_col(file_per,c)

        data_visual_obj.data_retention_per()
        data_visual_obj.data_gen_per()
        data_visual_obj.data_gen_per_atr()
        data_visual_obj.data_retention_per_atr()
        data_visual_obj.per_gen_atr()






if __name__ == '__main__':
    main_prog()
