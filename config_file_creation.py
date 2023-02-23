from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

config_object["data"] = {
    "time_in_middle": 20,
    "time_trail_preceed": 0.05
}

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)