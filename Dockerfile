
FROM python:3.9-slim

# Устанавливаем git и копируем репозиторий YOLOv5
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Клонируем YOLOv5 и устанавливаем зависимости
RUN git clone https://github.com/ultralytics/yolov5.git /app/yolov5 && \
    pip install --no-cache-dir -r /app/yolov5/requirements.txt pandas

# Копируем наш скрипт
COPY detect_and_count.py /app/

# Создаём папку для результатов
RUN mkdir -p /app/results

# По умолчанию запускаем скрипт
CMD ["python", "detect_and_count.py"]
