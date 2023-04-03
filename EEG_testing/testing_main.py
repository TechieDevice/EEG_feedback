# -*- coding: cp1251 -*-
import PySimpleGUI as sg
import numpy as np
import testing_disp

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

    while True:
        event, values = window.Read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-START-':
            disp_window(window)

    window.Close()

if __name__ == '__main__':
    main()