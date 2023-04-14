import numpy as np
import os
import pyedflib
import json
from datetime import datetime


def write_data(info, eeg_data, eeg_events):
    date = current_dateTime = datetime.now()
    filename = 'eeg-{}.edf'.format(date.strftime("%d-%m-%y_%H-%M"))
    file = os.path.join('.', filename)
    writer = pyedflib.EdfWriter(file, len(info)-1, file_type=pyedflib.FILETYPE_EDFPLUS)

    channel_info = []
    data_list = []

    for ch in range(len(info)-1):
        ch_dict = {'label': info[ch+1], 
                   'dimension': 'uV', 
                   'sample_frequency': int(info[0]),
                   'physical_max': np.max(eeg_data), 
                   'physical_min': np.min(eeg_data),  
                   'digital_max': 32767, 
                   'digital_min': -32768}
        channel_info.append(ch_dict)
        data_list.append(eeg_data[ch])

    writer.setSignalHeaders(channel_info)
    writer.writeSamples(data_list)

    for ev in eeg_events:
        writer.writeAnnotation(int(ev[0])/int(info[0]), -1, ev[1])

    writer.close()

    with open('data-{}.json'.format(date.strftime("%d-%m-%y_%H-%M")), 'w', encoding='utf-8') as f:
        json.dump(eeg_data.tolist(), f, 
                  separators=(',', ':'), 
                  sort_keys=True, 
                  indent=4)