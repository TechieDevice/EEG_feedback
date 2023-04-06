# -*- coding: cp1251 -*-
import PySimpleGUI as sg
import numpy as np
import testing_disp

import mne

def disp_window(window):
    window.Hide()
    testing_disp.main()
    window.UnHide()


layout = [
     [
         sg.Text('Задание на нахождение среднего квадратического \n отклонения дискретной случайной величины', 
                 size=(45, 2), 
                 key='-text-', 
                 font='Helvetica')
     ],
     [
        sg.Button('Начать',
               enable_events=True, 
               key='-START-', 
               font='Helvetica')
     ]
]

def main():
    window = sg.Window('Window', layout, size=(550,300))
    
    #file = "C:\\Users\Ilya Kovalev\\Documents\\NeuroPlayPro\\2023.04.06-16.45.43.600.edf"
    #data = mne.io.read_raw_edf(file)
    #raw_data = data.get_data()

    while True:
        event, values = window.Read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-START-':
            disp_window(window)

    window.Close()

if __name__ == '__main__':
    main()