# coding: utf-8
import PySimpleGUI as sg
import numpy as np
import requests
from threading import Event
import json
import time
import mne_func

def prepare():
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

def grab_data(stop_event, info, window):
    repeat = 0
    count = 0
    eeg_data = np.zeros(shape=(8, 1))
    while True:
        try:
            r = requests.get('http://127.0.0.1:2336/grabRawData')
        except:
            time.sleep(2)
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

        eeg_data = np.concatenate((eeg_data, new_data), axis=1)

        r.close()

        if count > 400:
            count = 0
            a_f, b_f, a_o, b_o = mne_func.preprocess(eeg_data, info)
            eeg_data = np.zeros(shape=(8, 1))
            
            #' gammaF='+str(round(g_f, 5))+\
            #' thetaC='+str(round(t_c, 5))
            sign = 'alphaF='+str(round(a_f, 5))+\
                   ' betaF='+str(round(b_f, 5))+\
                   '\n'+'alphaO='+str(round(a_o, 5))+\
                   ' betaO='+str(round(b_o, 5))              
            window['-SIGN-'].update(sign)
            #if a > b:
            #    window['-SIGN-'].update('CОСРЕДОТОЧТЕСЬ!!!')
            #else:
            #    window['-SIGN-'].update('Все хорошо')
            window.refresh()


        if stop_event.is_set():
            break
        
        count += 1
        time.sleep(1/1000)