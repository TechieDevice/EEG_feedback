# -*- coding: cp1251 -*-
import PySimpleGUI as sg
import random as rd
import threading
import eeg_receiver


def func(value, s):
    if value == s:
        con = sg.popup_yes_no('Верный ответ \n Запустить следующее задание?')
    else:
        con = sg.popup_yes_no('Неверный ответ, верный = {} \n Запустить следующее задание?'.format(s))
    return con


def generate():
    data = []
    row = ['X']
    for i in range(4):
        item = rd.randint(-10, 10)
        row.append(item)
    data.append(row.copy())
    row = ['p']
    m = 0
    m2 = 0
    n = 1.0
    for i in range(3):
        item = float('{:.2f}'.format(rd.uniform(0.01, n-0.03)))
        row.append(item)
        n = n - item
        m = data[0][i+1] * item + m
        m2 = data[0][i+1]**2 * item + m2
    row.append(float('{:.2f}'.format(n)))
    data.append(row.copy())
    row.clear()
    m = data[0][4] * n + m
    m2 = data[0][4]**2 * n + m2
    s = float('{:.2f}'.format((m2 - m**2)**0.5))
    data.append(s)
    return data


def fill_table(data, window):
    window['-ANSWER-'].Update('')
    for j in range(2):
        for i in range(5):
            window[str(j*5+i+1)].Update(data[j][i])


def main(): 
    data = generate()

    data_table = [sg.Text(key = '-TABLE-')]

    for j in range(2):
        row = []
        for i in range(5):
            row.append(sg.Text(data[j][i], 
                 key = str(j*5+i+1),
                 size=(4,1), 
                 background_color='#808080', 
                 pad=(1,1)))
        data_table.append(row)

    layout = [
         [
             sg.Text('Найти среднее квадратическое отклонение \n дискретной случайной величины Х, заданной \n законом распределения в таблице. \n Округлите ответ до 2 знаков после запятой.',
                    size=(40, 4),
                    font='Helvetica')
         ],
         [
             data_table
         ],
         [
             sg.Input(key='-ANSWER-', size=(10, 1)),
             sg.Button('Ответить',
                   enable_events=True, 
                   key='-FUNCTION-', 
                   font='Helvetica')
         ]
    ]

    window = sg.Window('Window', layout)

    stop_event = threading.Event()
    eeg_receiver.prepare()
    grab_thread = threading.Thread(target=eeg_receiver.grab_data, args=(stop_event,))
    grab_thread.start()

    while True:
        event, values = window.read()
        print(event, values)
        if event == '-FUNCTION-':
            if values['-ANSWER-'] == '':
                continue
            try:
                con = func(float(values['-ANSWER-']), data[2])
                if con == "No":
                    break
                else:
                    data = generate()
                    fill_table(data, window)
            except:
                sg.PopupOK('Используйте точку, как разделитель')

        if event == sg.WIN_CLOSED:
            break

    stop_event.set()
    grab_thread.join()
    window.Close()
