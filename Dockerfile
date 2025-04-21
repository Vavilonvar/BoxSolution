FROM python:3.9-slim

# Устанавливаем системные библиотеки (git + OpenCV-зависимости)
RUN apt-get update && \
    apt-get install -y git libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Клонируем YOLOv5 и ставим зависимости
RUN git clone https://github.com/ultralytics/yolov5.git /app/yolov5 && \
    pip install --no-cache-dir -r /app/yolov5/requirements.txt pandas

# Копируем твой скрипт
COPY detect_and_count.py /app/

# Создаём папку для результатов
RUN mkdir -p /app/results

CMD ["python", "detect_and_count.py"]
