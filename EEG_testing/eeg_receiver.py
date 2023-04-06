# -*- coding: cp1251 -*-
import PySimpleGUI as sg
import numpy as np
import requests
from threading import Event
import json

def prepare():
    r = requests.get('http://127.0.0.1:2336/enableDataGrabMode')
    requests.get('http://127.0.0.1:2336/grabRawData')
    json_r = json.loads(r.text)
    data = json_r["result"]
    print(data)

def grab_data(stop_event):
    while True:
        r = requests.get('http://127.0.0.1:2336/grabRawData')
        json_r = json.loads(r.text)
        new_data = json_r["data"]
        if len(new_data[0]) == 0:
            continue

        if stop_event.is_set():
            break