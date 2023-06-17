import pandas as pd
import os
class DataValidation:
    '''
    Here, the data is validated against all the conditions present for various scenarios given at
    https://stuprogit.iao.fraunhofer.de/erizt/erizt/-/blob/master/eventdetection.py
    '''

    def __init__(self, data, event_folder, start=300):
        self.event_col = ["HR (bpm)", "T1 (°C)", "SPO2 (%)", "CO2 (mmHg)", "AWRR (rpm)"]
        self.start = start
        self.event_folder = event_folder
        self.filename = data
        self.data = pd.read_csv(data, index_col=0)
        if self.data.shape[0]>start:
            self.means_start = self.data[:start].mean(axis = 0)
        else:
            self.start = int(self.data.shape[0]*0.1)
            self.means_start = self.data[:self.start].mean(axis = 0)
        self.report = self.data.copy()
        self.report[self.data.columns] = ''

    def read_event_file(self):
        file_to_read = self.filename
        if file_to_read[:file_to_read.rfind('/')]==self.event_folder:
            self.report = pd.read_csv(file_to_read, index_col=0)

    def write_event_file(self):
        folder_to_write = self.event_folder
        if not os.path.exists(folder_to_write):
            os.mkdir(folder_to_write)
        if self.filename[-10:]!='_event.csv':
            file_write = self.filename[self.filename.rfind('/')+1:-4]+"_event.csv"
            self.filename = folder_to_write + "/" + file_write
        else:
            file_write = self.filename
        self.report.to_csv(self.filename)
        file_excel = self.filename[:-4]+".xlsx"
        self.report.to_excel(file_excel)

    def detect_event_HR(self):
        self.read_event_file()
        desc = 'HR - Deviation is more than 20%'
        avg_val = self.means_start["HR (bpm)"]
        data_focus = self.data["HR (bpm)"][self.start:]
        for idx,i in enumerate(data_focus):
            val = i
            dev = abs((val - avg_val)) / val
            if dev > 0.2:
                self.report['HR (bpm)'][self.start+idx] = desc
        self.write_event_file()
    def detect_event_T1(self, high=40, low=36):
        self.read_event_file()
        high_desc = 'T1 - Temp is too high'
        low_desc = 'T1 - Temp is too low'
        data_focus = self.data["T1 (°C)"][self.start:]
        for idx,i in enumerate(data_focus):
            val = i
            if val> high:
                self.report["T1 (°C)"][self.start+idx] = high_desc
            elif val < low:
                self.report["T1 (°C)"][self.start+idx] = low_desc
        self.write_event_file()

    def detect_event_SPO2(self):
        self.read_event_file()
        low_desc = "SPO2 below 90 %"
        data_focus = self.data["SPO2 (%)"][self.start:]
        for idx,i in enumerate(data_focus):
            val = i
            if val < 90:
                self.report["SPO2 (%)"][self.start+idx] = low_desc
        self.write_event_file()
    def detect_event_CO2(self, high=40, low=36):
        self.read_event_file()
        high_desc = 'CO2 - CO2 pressure is too high'
        low_desc = 'CO2 - CO2 pressure is too low'
        data_focus = self.data["CO2 (mmHg)"][self.start:]
        for idx,i in enumerate(data_focus):
            val = i
            if val> high:
                self.report["CO2 (mmHg)"][self.start+idx] = high_desc
            elif val < low:
                self.report["CO2 (mmHg)"][self.start+idx] = low_desc
        self.write_event_file()

    def detect_event_AWRR(self):
        self.read_event_file()
        desc = 'AWRR - Deviation is more than 20%'
        avg_val = self.means_start["AWRR (rpm)"]
        data_focus = self.data["AWRR (rpm)"][self.start:]
        for idx,i in enumerate(data_focus):
            val = i
            dev = abs((val - avg_val)) / val
            if dev > 0.2:
                self.report['AWRR (rpm)'][self.start+idx] = desc
        self.write_event_file()
