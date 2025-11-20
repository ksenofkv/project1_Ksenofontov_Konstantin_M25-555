
# labyrinth_game/utils.py

from .constants import ROOMS

def describe_current_room(game_state):
    """
    Описывает текущую комнату.
    :param game_state: Словарь состояния игры.
    """
    # Получаем название текущей комнаты из состояния игры
    current_room = game_state['current_room']
    # Получаем данные комнаты из словаря ROOMS
    room_data = ROOMS.get(current_room, {})

    # Выводим название комнаты в верхнем регистре
    print(f"== {current_room.upper()} ==")

    # Выводим описание комнаты
    description = room_data.get('description', 'Описание комнаты не найдено.')
    print(description)

    # Выводим список видимых предметов
    items = room_data.get('items', [])
    if items:
        print(f"Заметные предметы: {', '.join(items)}")

    # Выводим доступные выходы
    exits = room_data.get('exits', {})
    if exits:
        print("Выходы:", ', '.join(exits.keys()))

    # Выводим сообщение о наличии загадки
    puzzle = room_data.get('puzzle', None)
    if puzzle is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def get_room_exits(room_name):
    """
    Возвращает словарь выходов для указанной комнаты.
    :param room_name: Название комнаты (например, 'entrance').
    :return: Словарь выходов (например, {'north': 'hall', 'east': 'trap_room'}).
    """
    # Получаем данные комнаты из словаря ROOMS
    room_data = ROOMS.get(room_name, {})
    # Возвращаем ключ 'exits', если он есть, иначе — пустой словарь
    return room_data.get('exits', {})

def get_room_items(room_name):
    """
    Возвращает список предметов в указанной комнате.
    :param room_name: Название комнаты (например, 'entrance').
    :return: Список предметов (например, ['torch', 'key']).
    """
    # Получаем данные комнаты из словаря ROOMS
    room_data = ROOMS.get(room_name, {})
    # Возвращаем ключ 'items', если он есть, иначе — пустой список
    return room_data.get('items', [])


def get_room_puzzle(room_name):
    """
    Возвращает загадку комнаты (вопрос и ответ).
    :param room_name: Название комнаты (например, 'hall').
    :return: Кортеж (вопрос, ответ) или None, если загадки нет.
    """
    # Получаем данные комнаты из словаря ROOMS
    room_data = ROOMS.get(room_name, {})
    # Возвращаем ключ 'puzzle', если он есть, иначе — None
    return room_data.get('puzzle', None)

