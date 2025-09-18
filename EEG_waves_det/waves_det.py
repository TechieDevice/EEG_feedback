# coding: utf-8
import PySimpleGUI as sg
import random as rd
import numpy as np
import threading
import eeg_receiver
import edf_writer

def main(): 
    
    layout = [
         [
             sg.Text('Запись идет',
                    size=(40, 4),
                    font='Helvetica',
                    background_color='#DAE0E6',
                    text_color='#444444')
         ],
         [
             sg.Text('xxx',
                    key='-SIGN-',
                    size=(40, 4),
                    font='Helvetica',
                    background_color='#DAE0E6',
                    text_color='#444444')
         ],
         [
             sg.Button('Остановить запись',
                   enable_events=True, 
                   key='-STOP-', 
                   font='Helvetica',
                   button_color='#444444 on #BDD0D6')
         ]
    ]

    window = sg.Window('EEG READER', layout, background_color='#DAE0E6')

    info = eeg_receiver.get_information()
    if len(info) == 0:
        sg.PopupOK('Отсутствует соединение с NeuroPlayPro')
        return
    eeg_receiver.prepare()
    
    stop_event = threading.Event()
    #is_con_event = threading.Event()
    grab_thread = threading.Thread(target=eeg_receiver.grab_data, args=(stop_event, info, window))
    grab_thread.start()

    shape = 0
    while True:
        event, values = window.read()

        if event == '-STOP-':
            break

        if event == sg.WIN_CLOSED:
            break

    #eeg_data = np.empty(shape=[8,1])
    stop_event.set()
    grab_thread.join()

    #edf_writer.write_data(info, eeg_data, eeg_events)
    window.Close()
