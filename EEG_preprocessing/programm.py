import time
import numpy as np
import requests
from PIL import ImageGrab
import os
import pyedflib
from datetime import datetime

# Функция для сравнения двух изображений
def images_are_different(img1, img2):
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    return not np.array_equal(arr1, arr2)

# Функция для снятия скриншота
def capture_screenshot():
    screenshot = ImageGrab.grab()
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # Форматируем временную метку
    return screenshot, timestamp

# Функция для активации режима захвата данных
def enable_data_grab_mode():
    try:
        response = requests.post('http://127.0.0.1:2336/enableDataGrabMode')
        response.raise_for_status()  # Проверяем успешность запроса
        print("Режим захвата данных активирован.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка активации режима захвата данных: {e}")
        return False

# Функция для получения данных ЭЭГ
def get_eeg_data():
    try:
        response = requests.get('http://127.0.0.1:2336/grabRawData')
        response.raise_for_status()  # Проверка на ошибки HTTP-запроса
        
        # Проверка структуры ответа
        response_json = response.json()
        if 'data' in response_json:
            eeg_data = np.array(response_json['data'])
            return eeg_data
        else:
            print(f"Ключ 'data' не найден в ответе: {response_json}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения данных ЭЭГ: {e}")
        return None

# Функция для записи данных ЭЭГ в формат EDF
def save_eeg_to_edf(eeg_data, timestamp, save_path):
    date = datetime.now()
    filename = f"eeg_{timestamp}.edf"
    file_path = os.path.join(save_path, filename)
    
    # Создаем writer для записи в EDF
    writer = pyedflib.EdfWriter(file_path, len(eeg_data), file_type=pyedflib.FILETYPE_EDFPLUS)
    
    # Создаем метаданные для каналов (параметры сигналов)
    channel_info = []
    for ch in range(len(eeg_data)):
        ch_dict = {
            'label': f'EEG channel {ch+1}',
            'dimension': 'uV',
            'sample_frequency': 125,  # Вы можете изменить частоту дискретизации
            'physical_max': np.max(eeg_data),
            'physical_min': np.min(eeg_data),
            'digital_max': 32767,
            'digital_min': -32768
        }
        channel_info.append(ch_dict)

    # Устанавливаем параметры сигналов и записываем данные
    writer.setSignalHeaders(channel_info)
    writer.writeSamples(eeg_data)

    # Закрываем файл
    writer.close()
    print(f"Данные ЭЭГ сохранены в: {file_path}")

# Основная функция
def main(save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Активируем режим захвата данных перед началом работы
    if not enable_data_grab_mode():
        print("Не удалось активировать режим захвата данных. Завершение программы.")
        return

    previous_image = None

    while True:
        # 1. Снятие скриншота
        screenshot, timestamp = capture_screenshot()

        # 2. Получение данных ЭЭГ
        eeg_data = get_eeg_data()

        if eeg_data is None:
            print("Ошибка получения данных ЭЭГ.")
            continue
        
        # 3. Проверка на дублирование скриншотов
        if previous_image is None or images_are_different(previous_image, screenshot):
            # Сохраняем скриншот в файл
            img_filename = f"screenshot_{timestamp}.png"
            screenshot.save(os.path.join(save_path, img_filename))
            print(f"Скриншот сохранён: {img_filename}")

            # Сохраняем данные ЭЭГ в EDF файл
            save_eeg_to_edf(eeg_data, timestamp, save_path)

            # Обновляем предыдущий скриншот
            previous_image = screenshot
        
        # Задержка в 0.1 секунду
        time.sleep(0.1)

# Задаём путь для сохранения скриншотов и данных
save_path = "C:/1MainYOLO/Results/01screen"

if __name__ == "__main__":
    main(save_path)
