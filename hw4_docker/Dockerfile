# Стадия 1: Builder (Сборка зависимостей)
FROM python:3.9-slim AS builder
WORKDIR /app

# Копируем файл с зависимостями приложения
COPY requirements.txt .

# Установка библиотек с использованием монтируемого кеша (требование задания)
# Флаг --user позволяет изолировать пакеты в папке пользователя /root/.local
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Стадия 2: Runtime (Финальный образ)
FROM python:3.9-slim
WORKDIR /app

# Информируем Docker о порте приложения и создаем точку монтирования для данных
EXPOSE 8000
VOLUME /app/data

# Переносим только установленные библиотеки из builder-стадии 
COPY --from=builder /root/.local /root/.local

# Копируем только исполняемый код приложения
COPY app.py .

# Добавляем путь к установленным библиотекам в переменную окружения PATH
ENV PATH=/root/.local/bin:$PATH

# Запуск веб-сервера uvicorn с доступом по внешнему интерфейсу
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]