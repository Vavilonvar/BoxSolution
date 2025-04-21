# BoxSolution
Solving the case from the YADRO™`s DubnaTECH

Этот репозиторий разворачивает детектор на базе **YOLOv5n** для подсчёта объектов (коробок) на фотографиях паллет. 
    После запуска `docker‑compose up --build` в каталоге `results/` генерируется CSV‑отчёт `results.csv` со статистикой по каждому подкаталогу в `images/`.

---
# Добавление нового типа коробки
Ниже приведён канонический пошаговый процесс расширения модели и кода для нового класса, например phone.

### Шаг 1 — Сбор данных
1. Сфотографируйте (синтезируйте) достаточное количество паллет, содержащих новый тип коробки.

### Шаг 2 — Разметка
1. Используйте любой аннотатор, совместимый с форматом YOLO (Например Roboflow).
2. В конфигурации проекта добавьте класс `phone` (порядок важен: индексы классов – это строки в names YOLO‑конфига).
3. Сохраняйте набор снимков и .txt метки в структуре:
   ```
     dataset/
     images/train/*.jpg
     labels/train/*.txt
     images/val/*.jpg
     labels/val/*.txt
   ```
### Шаг 3 — Обновление data.yaml
```
dataset: ../dataset
author: Someone
nc: 4            # NumberClass <-- было 3, стало 4
names: ["laptop", "tablet", "group_box", "phone"]
```
### Шаг 4 — Обучение/дообучение YOLOv5n
```
!python train.py \
  --img 640 \
  --batch 16 \
  --epochs 50 \
  --data /content/data/data.yaml \
  --weights yolov5n.pt \
  --name custom_yolov5n \
  --optimizer Adam
```
После обучения возьмите runs/train/new_boxes/weights/best.pt и положите в app/model/.
### Шаг 5 — Правка кода
> _Откройте `detect_and_count.py`._

1. Константа `COLUMNS_CSV`: добавьте новый столбец _в конец_ списка, например:
   ```
   COLUMNS_CSV = ['dir_name', 'laptop', 'tablet', 'group_box', 'phone']
   ```
2. Словарь `counts` (внутри detection_proccess) автоматически формируется из COLUMNS_CSV[1:], если скрипт написан как выше. Если использована фиксированная конструкция — добавьте ключ phone: 0.


-------------------------------
Рабочая структура 
![image](https://github.com/user-attachments/assets/541e60f1-1db8-48c6-a542-12ff1848c398)

