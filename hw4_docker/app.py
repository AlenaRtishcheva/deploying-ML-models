from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import datetime
import uvicorn
import random

# Создание приложения
app = FastAPI(title="API веб-сервера товаров (Inventory ML-App)")

# --- Блок подготовки базы данных
data = [['Антифриз EURO G11 (-45°С) зеленый, силикатный 5кг', 1025, 329, 11, 'c', 'антифриз', datetime.datetime(2026, 10, 16, 12, 36, 22)],
        ['Антифриз готовый фиолетовый Синтек MULTIFREEZE 5кг', 250, 315, 38, 'b', 'антифриз', datetime.datetime(2025, 12, 11, 8, 25, 31)],
        ['Антифриз G11 зеленый', 120, 329, 61, 'b', 'антифриз', datetime.datetime(2025, 6, 15, 15, 36, 30)],
        ['Антифриз Antifreeze OEM China OAT red -40 5кг', 390, 504, 65, 'c', 'антифриз', datetime.datetime(2025, 11, 30, 4, 12, 39)],
        ['Антифриз G11 зеленый', 135, 407, 93, 'b', 'антифриз', datetime.datetime(2026, 8, 25, 3, 24, 1)]]

df = pd.DataFrame(data)
df.columns = ['Наименование товара', 'Цена, руб.', 'cpm', 'Скидка', 'tp', 'Категория', 'dt']
df['Год'] = df['dt'].dt.year
df = df.drop(['cpm', 'tp', 'dt'], axis=1)

# Превращаем DataFrame в список словарей
items_db = []
for index, row in df.iterrows():
    items_db.append({
        "id": index + 1,
        "name": row['Наименование товара'],
        "price": row['Цена, руб.'],
        "discount": row['Скидка'],
        "category": row['Категория'],
        "year": row['Год']
    })

next_id = len(items_db) + 1

# --- Модели данных ---
class Item(BaseModel):
    name: str
    price: int = 0
    discount: int = 0
    category: str = 'антифриз'
    year: int = 2026

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    discount: Optional[int] = None
    category: Optional[str] = None
    year: Optional[int] = None

# --- Эндпоинты ---

@app.get("/")
def read_root():
    return {"status": "Active", "app": "Product API", "container": "Docker"}

@app.get("/items")
def get_all():
    return items_db

@app.get("/items/{id}")
def get_one(id: int, request: Request):
    item = next((i for i in items_db if i["id"] == id), None)
    if not item:
        raise HTTPException(404, "Товар не найден")
    
    # Обработка XML/JSON
    if request.headers.get('accept') == 'application/xml':
        xml = f'''<?xml version="1.0"?><item><id>{item["id"]}</id><name>{item["name"]}</name><price>{item["price"]}</price></item>'''
        return Response(content=xml, media_type="application/xml")
    return item

@app.post("/items", status_code=201)
def create(item: Item):
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    items_db.append(new_item)
    next_id += 1
    return new_item

@app.delete("/items/{id}", status_code=204)
def delete(id: int):
    global items_db
    items_db = [i for i in items_db if i["id"] != id]
    return