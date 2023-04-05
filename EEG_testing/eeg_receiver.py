# -*- coding: cp1251 -*-
import PySimpleGUI as sg
import numpy as np
import requests
import asyncio
import json

def prepare():
    requests.get('http://127.0.0.1:2336/enableDataGrabMode')
    requests.get('http://127.0.0.1:2336/grabRawData')

def grab_data(loop):
    r = requests.get('http://127.0.0.1:2336/grabRawData')
    json_r = json.loads(r.text)
    data = json_r["data"]
    print(data)