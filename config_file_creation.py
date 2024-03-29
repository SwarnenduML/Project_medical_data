from configparser import ConfigParser

#Get the configparser object
def create_config_file():
    config_object = ConfigParser()

    config_object["data"] = {
        "time_in_middle": 20, # explainability is issue
        "time_trail_preceed": 1, #0.05 1 - fully take everything, closer to 0 is reject everything - hw much data is allowed to be worked with
        # cobimaed percentage should be reflected here - Need
        "shifting" : 4, # change the name to regression window
        "threshold" : 0.2,
        "folder_to_read" : "C:/Users/sengupta/Downloads/erizt_data",
        "folder_to_write" : "C:/Users/sengupta/Downloads/erizt_data_generated",
        "folder_to_plot" : "C:/Users/sengupta/Downloads/plots",
        "data_gen" : True,
        "data_stat" : True,
        "data_visualize" : True,
        "data_for_visual" : "003-210525-185548.csv"
    }
    config_file_name = 'config.ini'
    #Write the above sections to config.ini file
    with open(config_file_name, 'w') as conf:
        config_object.write(conf)

    return config_file_name