
# labyrinth_game/utils.py

from .constants import ROOMS, TREASURE_CODE  # Импортируем словарь ROOMS и правильный код

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



def solve_puzzle(game_state):
    """
    Позволяет игроку решить загадку в текущей комнате.
    :param game_state: Словарь состояния игры.
    """
    current_room = game_state['current_room']
    
    # Получаем загадку из текущей комнаты
    puzzle = get_room_puzzle(current_room)
    
    # Проверяем, есть ли загадка в комнате
    if puzzle is None:
        #print("Загадок здесь нет.")
        return
    
    # Распаковываем кортеж (вопрос, ответ)
    question, answer = puzzle
    
    # Выводим вопрос загадки
    print(question)
    
    # Получаем ответ от игрока
    user_answer = input("Ваш ответ: ").strip().lower()
    
    # Проверяем, правильный ли ответ
    if user_answer == answer.lower():
        print("Правильно! Загадка решена.")
        
        # Убираем загадку из комнаты, чтобы её нельзя было решить дважды
        ROOMS[current_room]['puzzle'] = None
        
        # Добавляем игроку награду (например, предмет)
        game_state['player_inventory'].append('treasure_key')
        print("Вы получили ключ!")
    else:
        print("Неправильно. Попробуйте ещё раз.")


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 


def attempt_open_treasure(game_state):
    """
    Реализует логику открытия сундука.
    :param game_state: Словарь состояния игры.
    """
    current_room = game_state['current_room']
    
    # Проверяем, находится ли игрок в комнате с сундуком
    if current_room != 'treasure_room':
        #print("Здесь нет сундука.")
        return
    
    # Проверяем, есть ли у игрока ключ
    if 'treasure_key' in game_state['player_inventory']:
        # Если ключ есть, открываем сундук
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        # Удаляем сундук из списка предметов комнаты
        room_items = get_room_items(current_room)
        if 'treasure_chest' in room_items:
            room_items.remove('treasure_chest')
        # Устанавливаем флаг победы
        game_state['game_over'] = True
        print("В сундуке сокровище! Вы победили!")
        return
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. Вы можете попробовать ввести код.")
    user_input = input("Хотите ввести код? (да/нет): ").strip().lower()
    
    if user_input == 'да':
        # Запрашиваем код у игрока
        code = input("Введите код: ").strip().lower()
        
        # Сравниваем введённый код с правильным
        if code == TREASURE_CODE:
            # Если код верный, открываем сундук
            print("Вы ввели правильный код. Сундук открыт!")
            # Удаляем сундук из списка предметов комнаты
            room_items = get_room_items(current_room)
            if 'treasure_chest' in room_items:
                room_items.remove('treasure_chest')
            # Устанавливаем флаг победы
            game_state['game_over'] = True
            print("В сундуке сокровище! Вы победили!")
        else:
            # Если код неверный, сообщаем об этом
            print("Неверный код. Сундук не открывается.")
    else:
        # Если игрок отказался вводить код
        print("Вы отступаете от сундука.")