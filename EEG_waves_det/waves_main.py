# coding: utf-8
import PySimpleGUI as sg
import numpy as np
import waves_det

def start(window):
    window.Hide()
    waves_det.main()
    window.UnHide()


layout = [
     [
         sg.Text('Биологическая обратная связь на основе ЭЭГ', 
                 size=(45, 2), 
                 key='-text-', 
                 font='Helvetica',
                 background_color='#DAE0E6',
                 text_color='#444444')
     ],
     [
        sg.Button('Начать запись',
               enable_events=True, 
               key='-START-', 
               font='Helvetica',
               button_color='#444444 on #BDD0D6')
     ],
]

def main():
    window = sg.Window('EEG-data reciever', layout, size=(550,300), background_color='#DAE0E6')

    while True:
        event, values = window.Read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-START-':
            start(window)

    window.Close()

if __name__ == '__main__':
    main()
