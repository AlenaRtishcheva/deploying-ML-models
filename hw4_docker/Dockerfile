# Стадия 1: Builder (Сборка зависимостей)
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Стадия 2: Runtime (Финальный образ)
FROM python:3.9-slim
WORKDIR /app

# Критерии (сети и тома хранения)
EXPOSE 8000
VOLUME /app/data

# Копируем только результат установки библиотек из первой стадии (Builder)
COPY --from=builder /root/.local /root/.local
# Копируем исходный код приложения
COPY app.py .

# Настраиваем переменную окружения PATH, чтобы система видела установленный uvicorn
ENV PATH=/root/.local/bin:$PATH

# Команда запуска сервера: используем uvicorn для запуска объекта app из файла app.py
# --host 0.0.0.0 позволяет принимать подключения извне контейнера
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]