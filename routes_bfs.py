"""Вариант 19. Кратчайший маршрут в невзвешенном графе — повышенный уровень."""
from collections import deque
import json
from pathlib import Path

DATA_FILE = Path("routes_graph.json")
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "G"],
    "E": ["B", "G"],
    "F": ["C", "G"],
    "G": ["D", "E", "F", "H"],
    "H": ["G"]
}

def shortest_path(start, target, adjacency):
    """Возвращает кратчайший путь (список вершин) или None, если пути нет."""
    if start not in adjacency or target not in adjacency:
        return None
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == target:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return list(reversed(path))
        for neighbor in adjacency[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    return None

def save_graph(adjacency):
    DATA_FILE.write_text(json.dumps(adjacency, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    print("Граф маршрутов:", graph)
    start = input("Начальная вершина: ").strip().upper()
    target = input("Конечная вершина: ").strip().upper()
    path = shortest_path(start, target, graph)
    if path:
        print("Кратчайший путь:", " -> ".join(path))
        print("Длина пути (ребер):", len(path) - 1)
    else:
        print("Путь не найден: проверьте вершины или связность графа.")
    save_graph(graph)
    print(f"Граф сохранен в {DATA_FILE}")

if __name__ == "__main__":
    main()
