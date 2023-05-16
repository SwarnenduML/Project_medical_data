import pandas as pd
import warnings
import data_statistics
warnings.filterwarnings("ignore")
import yaml
from list_files import ListFiles
#from configparser import ConfigParser

import new_data_generation
import data_visual

def main_prog():
    # Read the configuration file - the configuration file here is read_yaml.yaml
    with open("req_yaml.yml", 'r') as stream:
        config_object = yaml.safe_load(stream)
    '''
    data_gen - tells us if there is a need to (re)generate the interpolated data or not
    data_stat - tells us if there is a need to (re)create the summary and statistics of the input and output data
    data_visualize - tells us if there is a need to visualize the data or not
    '''
    data_gen = config_object["data_gen"]
    data_stat = config_object["data_stat"]
    data_visualize = config_object["data_visualize"]
    event = config_object['event_logger']
    if data_gen:
        # if there is a need to create data
        data_generator_obj = new_data_generation.NewDataGeneration(config_object)
        data_generator_obj.create_data()
    if data_stat:
        # if there is a need to create the summary and statistics
        data_stat_obj = data_statistics.DataStatistics(config_object)
        compiled_data, valid_data = data_stat_obj.get_statistics()
    if data_visualize:
        # if there is a need to visualise the summary
        if not data_stat:
            # if statistics has not been taken in the program, then read the summary file and valid data file
            # previously created
            compiled_data = pd.read_csv(config_object["folder_to_write"] + "/total_summary_of_data.csv",
                                        index_col=0)
            valid_data = pd.read_csv(config_object["folder_to_write"] + "/total_summary_of_valid_data.csv",
                                        index_col=0)
        # read data inserted
        data_inserted = pd.read_csv(config_object["folder_to_write"] +'/data_inserted_csv.csv', index_col=0)

        data_visual_obj = data_visual.DataVisual(compiled_data,config_object,valid_data, data_inserted)
        data_visual_obj.tot_nulls_per() # Percentage of non-nulls per column per file before and after
        data_visual_obj.log_tot_nulls_per() # Log of percentage of non-nulls per column per file before and after
        data_visual_obj.non_null_per_file() # Percentage of non-nulls per file before and after
        data_visual_obj.create_comp() # Compare the input and output file for a particular file
        data_visual_obj.number_of_col_used() # Number of valid columns - combination of them
        data_visual_obj.column_type() # Number of valid columns individual
        data_visual_obj.visual_best_diff() # Visualises the best difference in numbers and percentage

        # Visualises the best difference in numbers and percentage per valid column
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

        data_visual_obj.data_retention_per() # Visualizes the data retention rate from the initial to the final one per file
        data_visual_obj.data_gen_per() # Visualizes the data generation rate from the initial to the final one per file
        data_visual_obj.data_gen_per_atr() # Visualizes the data generation rate from the initial to the final per attribute
        data_visual_obj.data_retention_per_atr() # Visualizes the data retention rate from the initial to the final per attribute
        data_visual_obj.per_gen_atr() # Distribution of data generation per attribute
        data_visual_obj.per_retention_atr() # Distribution of data retention per attribute


        # graph generation
        data_visual_obj.data_inserted_col() # Number of columns in entirity in which data was entered
        data_visual_obj.data_inserted_col_count() # Total number of data inserted per attribute
        data_visual_obj.data_inserted_col_count_mean() # Mean number of data inserted per attribute
        data_visual_obj.data_ins_atr() # Distribution of data inserted per attribute
    if event:
        lst_files = ListFiles(config_object)
        lst_files.files_with_col()






if __name__ == '__main__':
    main_prog()
