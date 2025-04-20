import os
import torch
import pandas as pd

# ==================================
#         Конфигурация путей
# ==================================

# Путь до фотографий
IMAGES_DIR = '/images'
# Путь для сохранения результатов
CSV_PATH = '/results/results.csv'
# Путь до весов модели
MODEL_PATH = '/app/model/best.pt'

# ==================================
#             Константы
# ==================================
# Устройство вычислений
DEVICE = 'cpu'
#  Допустимые расширения фотографий
FILENAME_EXTENSION = ('.png', '.jpg', '.jpeg')
# Структура результирующего CSV файла
COLUMNS_CSV = ['dir_name', 'laptop', 'tablet', 'group_box']


def detection_proccess(model_path, image_dir, result_dir):
    """
    Функция распознавания объектов на паллете.
      Функция основана на модели машинного зрения YOLO5_nano.
        model_path - путь к переобученной модели YOLO5_nano,
        image_dir - путь к директориям с фотографиями для распознавания
        result_dir - путь сохранения результирующего csv файла.
            
            Функция также использует константы:
                FILENAME_EXTENSION
                COLUMNS_CSV
    """
    # Инициализация модели
    model = torch.hub.load('/app/yolov5', 'custom', path=model_path, source='local')

    # Сбор результатов
    class_names = model.names  # список имён классов

    records = []
    # Обработка изображений
    for dir_name in os.listdir(image_dir):
        dir_path = os.path.join(image_dir, dir_name)
        # Проверка директорий
        if not os.path.isdir(dir_path):
            continue
        counts = {COLUMNS_CSV[1]: 0, COLUMNS_CSV[2]: 0, COLUMNS_CSV[3]: 0}
        for file_name in os.listdir(dir_path):
            # Проверка расширений
            if not file_name.lower().endswith(FILENAME_EXTENSION):
                continue
            img_path = os.path.join(dir_path, file_name)
            results = model(img_path)
            for *_, cls in results.xyxy[0].cpu().numpy():
                label = class_names[int(cls)]
                if label in counts:
                    counts[label] += 1
        records.append({COLUMNS_CSV[0]: dir_name, **counts})

    # Сохранение результатов
    df = pd.DataFrame(records, columns=COLUMNS_CSV)
    df.to_csv(result_dir, index=False)
    print(f'Результаты сохранены в {result_dir}')


if __name__ == '__main__':
    detection_proccess(model_path=MODEL_PATH, image_dir=IMAGES_DIR, result_dir=CSV_PATH)
