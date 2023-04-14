# coding: utf-8
import PySimpleGUI as sg
import numpy as np
import testing_rmsd

def disp_window(window, show_res):
    window.Hide()
    testing_rmsd.main(show_res)
    window.UnHide()


layout = [
     [
         sg.Text('Задание на нахождение среднего квадратического \n отклонения дискретной случайной величины', 
                 size=(45, 2), 
                 key='-text-', 
                 font='Helvetica',
                 background_color='#DAE0E6',
                 text_color='#444444')
     ],
     [
        sg.Button('Начать',
               enable_events=True, 
               key='-START-', 
               font='Helvetica',
               button_color='#444444 on #BDD0D6')
     ],
     [
        sg.Checkbox('Показывать ответ?',
               key='show_res', 
               font='Helvetica',
               background_color='#DAE0E6',
               text_color='#444444')
     ],
]

def main():
    window = sg.Window('EEG-data reciever', layout, size=(550,300), background_color='#DAE0E6')

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