# Используем образ Python в качестве базового образа
FROM python:3.10-slim

# Устанавливаем переменную окружения для предотвращения вывода сообщений
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем переменные окружения для языка и локали
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Устанавливаем зависимости проекта
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-rus \
        libgl1-mesa-glx --fix-missing\
    && rm -rf /var/lib/apt/lists/*

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

RUN mkdir -p /app/static/

# Собираем статические файлы Django
RUN python manage.py collectstatic --noinput

# Экспортируем порт, который будет слушать наш контейнер
EXPOSE 8081

# Запускаем сервер Django при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8081"]