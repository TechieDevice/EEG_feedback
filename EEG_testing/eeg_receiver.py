# coding: utf-8
import PySimpleGUI as sg
import numpy as np
import requests
from threading import Event
import json
import time

def prepare(ch_num):
    global eeg_data
    eeg_data = np.zeros(shape=(ch_num, 1))
    requests.get('http://127.0.0.1:2336/enableDataGrabMode')
    requests.get('http://127.0.0.1:2336/grabRawData')

def get_information():
    r = requests.get('http://127.0.0.1:2336/currentDeviceInfo')
    json_r = json.loads(r.text)
    info = []
    info.append(str(json_r["currentFrequency"]))
    channels = json_r["currentChannelsNames"]
    for ch in channels:
        info.append(ch)
    return info

def get_data():
    return eeg_data 

def grab_data(stop_event, lock):
    while True:
        r = requests.get('http://127.0.0.1:2336/grabRawData')
        json_r = json.loads(r.text)
        new_data = np.array(json_r["data"])
        if len(new_data[0]) == 0:
            continue
        
        with lock:
            global eeg_data
            eeg_data = np.concatenate((eeg_data, new_data), axis=1)

        r.close()
        if stop_event.is_set():
            break
        time.sleep(2/1000)