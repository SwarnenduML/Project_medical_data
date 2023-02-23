from configparser import ConfigParser

#Get the configparser object
def create_config_file():
    config_object = ConfigParser()

    config_object["data"] = {
        "time_in_middle": 20,
        "time_trail_preceed": 1#0.05
    }
    config_file_name = 'config.ini'
    #Write the above sections to config.ini file
    with open(config_file_name, 'w') as conf:
        config_object.write(conf)

    return config_file_name