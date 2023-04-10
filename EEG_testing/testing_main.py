# coding: utf-8
import PySimpleGUI as sg
import numpy as np
import testing_disp

import mne

def disp_window(window, show_res):
    window.Hide()
    testing_disp.main(show_res)
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
     ],
     [
        sg.Checkbox('Показывать ответ?',
               key='show_res', 
               font='Helvetica')
     ],
]

def main():
    window = sg.Window('Window', layout, size=(550,300))

    while True:
        event, values = window.Read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-START-':
            show_res = values['show_res']
            disp_window(window, show_res)

    window.Close()

if __name__ == '__main__':
    main()