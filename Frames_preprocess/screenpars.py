import os
import pyautogui
import keyboard
from datetime import datetime
from PIL import Image
import json
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle
import subprocess
#53


c_time = None
#mode = "teach"
#mode = "dataset"
mode = "work"

# Путь к папке с изображениями и файлами разметки
data_dir = 'C:\Users\Ilya\Documents\GitHub\EEG_feedback\Frames_preprocess\Frames_preprocess.pyproj\Dataset'

# Create the directory to store the screenshots
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def create_discr(now, filename1, cards = []):
    if cards == []:
        cards = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    data = {
        "filename": "screenshot_2023-03-04_09-44-46.png",
        "size": {
            "width": 2560,
            "height": 1440
        },
        "count": 9,	
        "objects": [
            {
            "label": cards[0],
            "bbox": {
                "xmin": 1340,
                "ymin": 915,
                "xmax": 1370,
                "ymax": 970
                }
            },
            {
            "label": cards[1],
            "bbox": {
                "xmin": 1340,
                "ymin": 970,
                "xmax": 1370,
                "ymax": 1005
                }
            },
            {
            "label": cards[2],
            "bbox": {   
                "xmin": 1400,
                "ymin": 910,
                "xmax": 1430,
                "ymax": 965
                }
            },
            {
            "label": cards[3],
            "bbox": {   
                "xmin": 1400,
                "ymin": 965,
                "xmax": 1430,
                "ymax": 1000
                }
            },
            {
            "label": cards[4],
            "bbox": {
                "xmin": 970,
                "ymin": 590,
                "xmax": 1000,
                "ymax": 645
                }
            },
            {
            "label": cards[5],
            "bbox": {
                "xmin": 970,
                "ymin": 645,
                "xmax": 1000,
                "ymax": 680
                }
            },
            {
            "label": cards[6],
            "bbox": {
                "xmin": 1097,
                "ymin": 590,
                "xmax": 1127,
                "ymax": 645
                }
            },
            {
            "label": cards[7],
            "bbox": {
                "xmin": 1097,
                "ymin": 645,
                "xmax": 1127,
                "ymax": 680
                }
            },
            {
            "label": cards[8],
            "bbox": {
                "xmin": 1225,
                "ymin": 590,
                "xmax": 1255,
                "ymax": 645
                }
            },
            {
            "label": cards[9],
            "bbox": {
                "xmin": 1225,
                "ymin": 645,
                "xmax": 1255,
                "ymax": 680
                }
            },
            {
            "label": cards[10],
            "bbox": {
                "xmin": 1352,
                "ymin": 590,
                "xmax": 1382,
                "ymax": 645
                }
            },
            {
            "label": cards[11],
            "bbox": {
                "xmin": 1352,
                "ymin": 645,
                "xmax": 1382,
                "ymax": 680
                }
            },
            {
            "label": cards[12],
            "bbox": {
                "xmin": 1480,
                "ymin": 590,
                "xmax": 1510,
                "ymax": 645
                }
            },
            {
            "label": cards[13],
            "bbox": {
                "xmin": 1480,
                "ymin": 645,
                "xmax": 1510,
                "ymax": 680
                }
            }
        ]
    }
    with open(filename1, 'w') as f:
        json.dump(data, f)


# Define the function to take a screenshot
def take_screenshot():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{data_dir}/screenshot_{now}.png'
    filename1 = f'{data_dir}/screenshot_{now}.txt'
    img = pyautogui.screenshot()
    img.save(filename)
    create_discr(now, filename1)
    print(f'Screenshot saved to {filename}')

# Define the function to take a screenshot
def take_screenshot_proc(n):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{data_dir}/new/screenshot_{now}.png'
    img = pyautogui.screenshot()
    img.save(filename)
    #now = '2023-03-04_09-44-46'
    #filename = data_dir+'/screenshot_2023-03-04_09-44-46.png'
    #img = Image.open(filename)
    im_card1_r = img.crop((1340, 915, 1370, 970)).resize((64, 64))
    im_card1_m = img.crop((1340, 970, 1370, 1005)).resize((64, 64))
    im_card2_r = img.crop((1400, 910, 1430, 965)).resize((64, 64))
    im_card2_m = img.crop((1400, 965, 1430, 1000)).resize((64, 64))
    im_table1_r = img.crop((970, 590, 1000, 645)).resize((64, 64))
    im_table1_m = img.crop((970, 645, 1000, 680)).resize((64, 64))
    im_table2_r = img.crop((1097, 590, 1127, 645)).resize((64, 64))
    im_table2_m = img.crop((1097, 645, 1127, 680)).resize((64, 64))
    im_table3_r = img.crop((1225, 590, 1255, 645)).resize((64, 64))
    im_table3_m = img.crop((1225, 645, 1255, 680)).resize((64, 64))
    im_table4_r = img.crop((1352, 590, 1382, 645)).resize((64, 64))
    im_table4_m = img.crop((1352, 645, 1382, 680)).resize((64, 64))
    im_table5_r = img.crop((1480, 590, 1510, 645)).resize((64, 64))
    im_table5_m = img.crop((1480, 645, 1510, 680)).resize((64, 64))
    images = [im_card1_r, im_card1_m, im_card2_r, im_card2_m, im_table1_r, im_table1_m, im_table2_r, im_table2_m, im_table3_r, im_table3_m, im_table4_r, im_table4_m, im_table5_r, im_table5_m]
    cards = get_index_to_label(model.predict(tf.stack(images)), unique_labels)
    answer = ''.join(cards)
    answer1 = ' '.join(cards)
    answer2 = ""

    # Используем цикл for для перебора всех символов в строке
    j = 0
    for i in range(len(answer1)):
        # Если текущий символ не пробел или его индекс четный, добавляем его в новую строку
        if answer1[i] != " ":
            answer2 += answer1[i]
        else:
            j+=1
            if j % 2 == 0:
                answer2 += answer1[i]
    filename2 = f'{data_dir}/new/screenshot_{answer}_{now}.png'
    os.rename(filename, filename2)
    filename1 = f'{data_dir}/new/screenshot_{answer}_{now}.txt'
    create_discr(now, filename1, cards)
    data = 'D:/Envs/venv_3_10_tf/Scripts/python.exe D:/Projects/Poker/texassim.py --c ' + answer2 + ' --n ' + str (n)
    print(data)
    returned_output = subprocess.check_output(data)
    print(returned_output)



def load_data(data_dir):
    image_files = os.listdir(data_dir)
    id = []
    id_full = []
    images = []
    images_full = []
    labels = []
    labels_count = []
    labels_sit = []
    labels_play = []
    # Читаем каждый файл разметки и изображение и добавляем его в соответствующий список
    for image_file in image_files:
        # Проверяем, что файл имеет расширение PNG
        if image_file.endswith('.png'):
            # Читаем файл разметки
            annotation_file = os.path.join(data_dir, image_file.replace('.png', '.txt'))
            with open(annotation_file, 'r') as f:
                annotation = json.load(f)
        
            # Читаем изображение
            image_path = os.path.join(data_dir, image_file)
            image = Image.open(image_path)
            id_full.append(image_path)
            images_full.append(image)
            i = 0
            # Обрабатываем каждый объект на изображении
            #labels_count.append((annotation['count']-5)/10)
            #labels_sit.append((annotation['sit']-5)/10)
            #labels_play.append((annotation['play']-5)/10)
            #print(labels_count)
            for obj in annotation['objects']:
                # Получаем координаты bbox
                xmin = obj['bbox']['xmin']
                ymin = obj['bbox']['ymin']
                xmax = obj['bbox']['xmax']
                ymax = obj['bbox']['ymax']
                id.append(image_file +'_'+str(i))
                i+=1
                # Вырезаем кусок изображения, соответствующий bbox
                cropped_image = image.crop((xmin, ymin, xmax, ymax))

                # Меняем размер изображения до 64x64
                resized_image = cropped_image.resize((64, 64))
                        
                # Добавляем изображение и метку в соответствующие списки
                images.append(resized_image)
                labels.append(obj['label'])
    #return(id, id_full, images, images_full, labels, labels_count, labels_sit, labels_play)
    return(id, images, labels)

def trans_labels(labels):
    # Список всех уникальных меток
    unique_labels = list(set(labels))

    # Создаем словарь для преобразования меток в числа
    label_to_index = {}
    for i, label in enumerate(unique_labels):
        label_to_index[label] = i

    # Преобразуем метки в числовой формат
    numeric_labels = [label_to_index[label] for label in labels]

    # Преобразуем числовые метки в one-hot encoding
    one_hot_labels = tf.keras.utils.to_categorical(numeric_labels)
    return(one_hot_labels, unique_labels)


def get_index_to_label(one_hot_labels, unique_labels):
    index_to_label = []
    for i in range(len(one_hot_labels)):
        index_to_label.append(unique_labels[np.argmax(one_hot_labels[i])])
    return index_to_label


def show_teach(history):
    # Получение значений лосс-функции и точности из истории обучения
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    accuracy = history.history['accuracy']
    val_accuracy = history.history['val_accuracy']

    # Отображение графика лосс-функции
    plt.figure()
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend()
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    #plt.show()
    
    # Отображение графика точности
    plt.figure()
    plt.plot(accuracy, label='Training Accuracy')
    plt.plot(val_accuracy, label='Validation Accuracy')
    plt.legend()
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    #plt.show()

# функция для отображения набора изображений в заданном формате
def show_images(images, test_ids, labels_true, labels_pred, n_cols=5):
    n_rows = len(images) // n_cols + (len(images) % n_cols > 0)
    plt.figure(figsize=(n_cols * 2, n_rows * 2))
    for i, (image, test_id, label_true, label_pred) in enumerate(zip(images, test_ids, labels_true, labels_pred)):
        plt.subplot(n_rows, n_cols, i + 1)
        plt.imshow(image)
        plt.axis('off')
        if label_true==label_pred:
            cl = 'black'
        else:
            cl = 'red'
        plt.title(f'{test_id}, True: {label_true}, Pred: {label_pred}', fontsize=6, color = cl)
    plt.tight_layout()
    plt.show()

if mode == "dataset":
    # Register the ho55ey to take the screenshot
    keyboard.add_hotkey('~', take_screenshot)

    # Start the keyboard listener
    keyboard.wait()


if mode == "work":

    model_filename = f'{data_dir}/model_2023-03-08_22-47-45.pickle'
    with open(model_filename, 'rb') as f:
        data_new = pickle.load(f)
    model = data_new['model']
    unique_labels = data_new['labels']

    prob = 0
    # Register the hotkey to take the screenshot
    keyboard.add_hotkey('2', lambda: take_screenshot_proc(2))
    keyboard.add_hotkey('3', lambda: take_screenshot_proc(3))
    keyboard.add_hotkey('4', lambda: take_screenshot_proc(4))
    keyboard.add_hotkey('5', lambda: take_screenshot_proc(5))
    keyboard.add_hotkey('6', lambda: take_screenshot_proc(6))
    keyboard.add_hotkey('7', lambda: take_screenshot_proc(7))
    keyboard.add_hotkey('8', lambda: take_screenshot_proc(8))
    keyboard.add_hotkey('9', lambda: take_screenshot_proc(9))

    # Start the keyboard listener
    keyboard.wait()




elif mode == "teach":
    #creating and teaching
    #id, id_full, images, images_full, labels, labels_count, labels_sit, labels_play = load_data(data_dir)
    id, images, labels = load_data(data_dir)
    one_hot_labels, unique_labels = trans_labels(labels)
    train_id, test_id, train_images, test_images, train_labels, test_labels = train_test_split(id, images, one_hot_labels, test_size=0.2)
    datagen = ImageDataGenerator(rotation_range=15, rescale=1./255)
    # datagen_full = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    # train_id_full, test_id_full, train_images_full, test_images_full, train_labels_full, test_labels_full = train_test_split(id_full, images_full, one_hot_labels, test_size=0.2)

    # model_full = tf.keras.Sequential([
    #     tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(2560, 1440, 3)),
    #     tf.keras.layers.MaxPooling2D((2, 2)),
    #     #tf.keras.layers.Dropout(0.5),
    #     tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    #     tf.keras.layers.MaxPooling2D((2, 2)),
    #     tf.keras.layers.Dropout(0.5),
    #     tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    #     tf.keras.layers.MaxPooling2D((2, 2)),
    #     tf.keras.layers.Dropout(0.5),
    #     tf.keras.layers.Flatten(),
    #     tf.keras.layers.Dense(128, activation='relu'),
    #     tf.keras.layers.Dropout(0.5),
    #     tf.keras.layers.Dense(1, activation='tanh')
    #     ])

    # model_full.compile(optimizer='adam',
    #               loss='mse',
    #               metrics=['accuracy'])


    # batch_size = 32
    # epochs = 200
    # #print(len(images))
    # steps_per_epoch = int(np.ceil(len(images) / batch_size))

    # # Обучаем модель
    # history = model_full.fit(
    #     datagen_full.flow(tf.stack(train_images_full), train_labels_full, batch_size=batch_size),
    #     #tf.stack(train_images),
    #     #train_labels,
    #     #steps_per_epoch=steps_per_epoch,
    #             #batch_size=32,
    #     validation_data = test_datagen.flow(tf.stack(test_images_full), test_labels_full), 
    #     epochs = epochs
    # )



    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        #tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(unique_labels), activation='softmax')
    ])
    # Компилируем модель
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    batch_size = 32
    epochs = 200
    #print(len(images))
    steps_per_epoch = int(np.ceil(len(images) / batch_size))

    # Обучаем модель
    history = model.fit(
        datagen.flow(tf.stack(train_images), train_labels, batch_size=batch_size),
        #tf.stack(train_images),
        #train_labels,
        #steps_per_epoch=steps_per_epoch,
                #batch_size=32,
        validation_data = test_datagen.flow(tf.stack(test_images), test_labels), 
        epochs = epochs
    )

    # Оцениваем качество модели на тестовом наборе данных
    test_loss, test_acc = model.evaluate(tf.stack(test_images), test_labels, verbose=2)
    print('Test accuracy:', test_acc)
    show_teach(history)

    # получение предсказанных меток с помощью нейронной сети model
    labels_pred = model.predict(tf.stack(test_images))
    #print(test_labels)

    id_test_label = get_index_to_label(test_labels, unique_labels)
    pred_test_label = get_index_to_label(labels_pred, unique_labels)
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    model_filename = f'{data_dir}/model_{now}.pickle'
    with open(model_filename, 'wb') as f:
        pickle.dump({'model': model, 'labels': unique_labels}, f)


    # отображение набора изображений с верными и предсказанными метками
    #show_images(images, np.argmax(test_labels, axis=1).tolist(), np.argmax(labels_pred, axis=1).tolist())
    show_images(test_images, test_id, id_test_label, pred_test_label)
    #show_images(images, true_labels, pred_labels)


