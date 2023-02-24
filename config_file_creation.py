from configparser import ConfigParser

#Get the configparser object
def create_config_file():
    config_object = ConfigParser()

    config_object["data"] = {
        "time_in_middle": 20,
        "time_trail_preceed": 1, #0.05 1 - fully take everything, closer to 0 is reject everything
        "shifting" : 4,
        "threshold" : 0.2,
        "folder_to_read" : "C:/Users/sengupta/Downloads/erizt_data",
        "folder_to_write" : "C:/Users/sengupta/Downloads/erizt_data_generated",
        "data_gen" : False,
        "data_stat" : False,
        "data_visualize" : True,
        "data_for_visual" : "name_of_excel"
    }
    config_file_name = 'config.ini'
    #Write the above sections to config.ini file
    with open(config_file_name, 'w') as conf:
        config_object.write(conf)

    return config_file_name