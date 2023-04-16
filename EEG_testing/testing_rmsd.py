# coding: utf-8
import PySimpleGUI as sg
import random as rd
import numpy as np
import threading
import eeg_receiver
import edf_writer


def res_check(value, s, show_res, eeg_events, lock):
    with lock:
            shape = eeg_receiver.get_data().shape[1]
    if value == s:
        if show_res == True:
            new_e = np.array(list([str(shape),'right_answer'])).reshape(1,2)
            con = sg.popup_yes_no('Верный ответ \n Запустить следующее задание?',
                                    background_color='#DAE0E6',
                                    text_color='#444444',
                                    button_color='#444444 on #BDD0D6')
        else:
            rnd = rd.randint(1, 10)
            if rnd > 3:
                new_e = np.array(list([str(shape),'right_answer'])).reshape(1,2)
                con = sg.popup_yes_no('Верный ответ \n Запустить следующее задание?',
                                      background_color='#DAE0E6',
                                      text_color='#444444',
                                      button_color='#444444 on #BDD0D6')
            else:
                new_e = np.array(list([str(shape),'fake_wrong_answer'])).reshape(1,2)
                con = sg.popup_yes_no('Неверный ответ \n Запустить следующее задание?',
                                      background_color='#DAE0E6',
                                      text_color='#444444',
                                      button_color='#444444 on #BDD0D6')
    else:
        new_e = np.array(list([str(shape),'wrong_answer'])).reshape(1,2)
        if show_res == True:
            con = sg.popup_yes_no('Неверный ответ, верный = {} \n Запустить следующее задание?'.format(s),
                                      background_color='#DAE0E6',
                                      text_color='#444444',
                                      button_color='#444444 on #BDD0D6')
        else:
            con = sg.popup_yes_no('Неверный ответ \n Запустить следующее задание?',
                                    background_color='#DAE0E6',
                                    text_color='#444444',
                                    button_color='#444444 on #BDD0D6')
    eeg_events = np.concatenate((eeg_events,new_e),axis=0)
    return con, eeg_events


def generate():
    task_data = []
    row = ['X']
    for i in range(4):
        item = rd.randint(-10, 10)
        row.append(item)
    task_data.append(row.copy())
    row = ['p']
    m = 0
    m2 = 0
    n = 1.0
    for i in range(3):
        item = float('{:.2f}'.format(rd.uniform(0.01, n-0.03)))
        row.append(item)
        n = n - item
        m = task_data[0][i+1] * item + m
        m2 = task_data[0][i+1]**2 * item + m2
    row.append(float('{:.2f}'.format(n)))
    task_data.append(row.copy())
    row.clear()
    m = task_data[0][4] * n + m
    m2 = task_data[0][4]**2 * n + m2
    s = float('{:.2f}'.format((m2 - m**2)**0.5))
    task_data.append(s)
    return task_data


def fill_table(task_data, window):
    window['-ANSWER-'].Update('')
    for j in range(2):
        for i in range(5):
            window[str(j*5+i+1)].Update(task_data[j][i])


def main(show_res): 
    task_data = generate()

    task_data_table = [sg.Text(key = '-TABLE-', background_color='#DAE0E6')]

    for j in range(2):
        row = []
        for i in range(5):
            row.append(sg.Text(task_data[j][i], 
                 key = str(j*5+i+1),
                 size=(4,1), 
                 background_color='#B0B0B0',
                 text_color='#444444',
                 pad=(1,1)))
        task_data_table.append(row)

    layout = [
         [
             sg.Text('Найти среднеквадратическое отклонение \n дискретной случайной величины Х, заданной \n законом распределения в таблице. \n Округлите ответ до 2 знаков после запятой.',
                    size=(40, 4),
                    font='Helvetica',
                    background_color='#DAE0E6',
                    text_color='#444444')
         ],
         [
             task_data_table
         ],
         [
             sg.Input(key='-ANSWER-', size=(10, 1)),
             sg.Button('Ответить',
                   enable_events=True, 
                   key='-FUNCTION-', 
                   font='Helvetica',
                   button_color='#444444 on #BDD0D6')
         ]
    ]

    window = sg.Window('Root mean square deviation', layout, background_color='#DAE0E6')

    stop_event = threading.Event()
    lock = threading.Lock()
    info = eeg_receiver.get_information()
    eeg_receiver.prepare(len(info)-1)
    eeg_events = np.array(list([str(1),'start task'])).reshape(1,2)
    shape = 0
    grab_thread = threading.Thread(target=eeg_receiver.grab_data, args=(stop_event, lock))
    grab_thread.start()

    while True:
        event, values = window.read()
        if event == '-FUNCTION-':
            if values['-ANSWER-'] == '':
                continue
            try:
                con, eeg_events = res_check(float(values['-ANSWER-']), task_data[2], show_res, eeg_events, lock)

                with lock:
                    shape = eeg_receiver.get_data().shape[1]
                new_e = np.array(list([str(shape),'end task'])).reshape(1,2)
                eeg_events = np.concatenate((eeg_events,new_e),axis=0)

                if con == "No":
                    break
                else:
                    task_data = generate()
                    fill_table(task_data, window)

                    with lock:
                        shape = eeg_receiver.get_data().shape[1]
                    new_e = np.array(list([str(shape),'start task'])).reshape(1,2)
                    eeg_events = np.concatenate((eeg_events,new_e),axis=0)
            except:
                lastElementIndex = len(eeg_events)-1
                eeg_events = eeg_events[:lastElementIndex]
                sg.PopupOK('Используйте точку, как разделитель')

        if event == sg.WIN_CLOSED:
            break

    eeg_data = np.empty(shape=[6,1])
    with lock:
        eeg_data = eeg_receiver.get_data()
    stop_event.set()
    grab_thread.join()

    edf_writer.write_data(info, eeg_data, eeg_events)
    window.Close()
