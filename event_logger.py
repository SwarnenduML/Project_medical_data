from data_validation import DataValidation

class EventLogger():
    def prog_start(self, file_to_operate, config_object):
        for x in file_to_operate:
            dv = DataValidation(x, config_object['folder_for_event_output'])
            dv.detect_event_HR()  # Event logging for heart beat
            high_t1 = config_object['high_T1']
            low_t1 = config_object['low_T1']
            dv.detect_event_T1(high=high_t1, low=low_t1)  # Event logging for temperature 1
            dv.detect_event_SPO2()  # Event logging for SPO2
            high_co2 = config_object['high_CO2']
            low_co2 = config_object['low_CO2']
            dv.detect_event_CO2(high=high_co2, low=low_co2)  # Event logging for pressure for CO2
            dv.detect_event_AWRR()  # Event logging for AirWay Respiratory Rate
            print(x + " event log generated")
