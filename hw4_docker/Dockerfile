# Стадия 1: Builder (Сборка зависимостей)
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Кеширование зависимостей через монтирование
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-cache-dir -r requirements.txt

# Стадия 2: Runtime (Финальный образ)
FROM python:3.9-slim
WORKDIR /app

# Сети и тома (согласно заданию)
EXPOSE 8000
VOLUME /app/data

# Копируем установленные пакеты 
COPY --from=builder /root/.local /root/.local
# Копируем код приложения
COPY app.py .

# Настройка окружения
ENV PATH=/root/.local/bin:$PATH

# Запуск приложения
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]