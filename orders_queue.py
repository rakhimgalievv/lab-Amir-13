"""Вариант 8. Система заказов — средний уровень."""
from collections import deque
import json
from pathlib import Path

DATA_FILE = Path("orders.json")
orders = deque()
completed = []

def add_order(order_id, description):
    if any(order["id"] == order_id for order in orders) or any(x["id"] == order_id for x in completed):
        return "Ошибка: такой номер заказа уже существует."
    orders.append({"id": order_id, "description": description})
    save_data()
    return f"Заказ {order_id} добавлен в очередь."

def serve_order():
    if not orders:
        return None
    order = orders.popleft()
    completed.append(order)
    save_data()
    return order

def find_order(order_id):
    return next((order for order in orders if order["id"] == order_id), None)

def remaining_report():
    return list(orders)

def save_data():
    DATA_FILE.write_text(json.dumps({"queue": list(orders), "completed": completed},
                                    ensure_ascii=False, indent=2), encoding="utf-8")

def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            orders.extend(data.get("queue", []))
            completed.extend(data.get("completed", []))
        except (json.JSONDecodeError, OSError):
            print("Файл данных поврежден; начата пустая сессия.")

def main():
    load_data()
    while True:
        print("\n1 — новый заказ | 2 — выдать первый | 3 — поиск по номеру | 4 — отчет | 0 — выход")
        choice = input("Выбор: ").strip()
        if choice == "1":
            order_id = input("Номер: ").strip()
            description = input("Описание: ").strip()
            print(add_order(order_id, description))
        elif choice == "2":
            order = serve_order()
            print(f"Выдан заказ: {order}" if order else "Очередь пуста.")
        elif choice == "3":
            found = find_order(input("Номер: ").strip())
            print(found if found else "Заказ не найден.")
        elif choice == "4":
            print("Осталось:", json.dumps(remaining_report(), ensure_ascii=False))
        elif choice == "0":
            break
        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    main()
