import pandas as pd
class DataValidation:
    '''
    Here, the data is validated against all the conditions present for various scenarios given at
    https://stuprogit.iao.fraunhofer.de/erizt/erizt/-/blob/master/eventdetection.py
    '''

    def __init__(self, data, start=300):
        self.event_col = ["HR (bpm)", "T1 (°C)", "SPO2 (%)", "CO2 (mmHg)", "AWRR (rpm)"]
        self.start = start
        self.data = pd.read_csv(data, index_col=0)
        if self.data.shape[0]>start:
            self.means_start = self.data[:start].mean(axis = 0)
        else:
            self.start = int(self.data.shape[0]*0.1)
            self.means_start = self.data[:self.start].mean(axis = 0)
        self.report = self.data.copy()
        self.report[self.event_col] = ''


    def detect_event_hr(self):
        desc = 'HR - Deviation is more than 20%'
        avg_val = self.means_start["HR (bpm)"]
        data_focus = self.data["HR (bpm)"][self.start:]
        for idx,i in enumerate(data_focus):
            val = i
            dev = abs((val - avg_val)) / val
            if dev > 0.2:
                self.report['HR (bpm)'][self.start+idx] = desc

    def detect_event_t1(self, high=40, low=36):
        high_desc = 'T1 - Temp is too high'
        low_desc = 'T1 - Temp is too low'
        data_focus = self.data["T1 (°C)"][self.start:]
        for idx,i in enumerate(data_focus):
            val = i
            if val> high:
                self.report["T1 (°C)"][self.start+idx] = high_desc
            elif val < low:
                self.report["T1 (°C)"][self.start+idx] = low_desc

