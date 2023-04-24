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
    info = []
    try:
        r = requests.get('http://127.0.0.1:2336/currentDeviceInfo')
    except:
        return info
    json_r = json.loads(r.text)
    info.append(str(json_r["currentFrequency"]))
    channels = json_r["currentChannelsNames"]
    for ch in channels:
        info.append(ch)
    return info

def get_data():
    return eeg_data 

def grab_data(stop_event, lock):
    repeat = 0
    while True:
        try:
            r = requests.get('http://127.0.0.1:2336/grabRawData')
        except:
            time.sleep(1)
            repeat += 1
            if repeat >= 3:
                ans = sg.popup_yes_no('Соединение потеряно. \n Повторить попытку соединения?',
                                    background_color='#DAE0E6',
                                    text_color='#444444',
                                    button_color='#444444 on #BDD0D6')
                if ans == "Yes":
                    repeat = 0
                else:
                    sg.PopupOK('Считывание данных прервано')
                    stop_event.set()
                    break
            continue

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