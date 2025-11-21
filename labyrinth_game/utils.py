
# labyrinth_game/utils.py

from labyrinth_game.constants import ROOMS, TREASURE_CODE, COMMANDS # Импортируем словарь ROOMS и др
import math  # Импортируем модуль math для использования тригонометрических функций

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
    
  # Создаем список альтернативных вариантов ответа
    # Например, если правильный ответ '10', то добавляем 'десять'
    alternative_answers = []
    if answer == '10':
        alternative_answers = ['десять', 'десять ', '10']
    elif answer == 'сказка':
        alternative_answers = ['сказка', 'сказка ', 'сказка.']
    # Добавьте другие альтернативы по мере необходимости

    # Проверяем, правильный ли ответ (включая альтернативы)
    if user_answer == answer.lower() or user_answer in alternative_answers:
        print("Правильно! Загадка решена.")
      
        # Убираем загадку из комнаты, чтобы её нельзя было решить дважды
        ROOMS[current_room]['puzzle'] = None
        
        # Добавляем игроку награду (например, предмет)
        game_state['player_inventory'].append('treasure_key')
        print("Вы получили ключ!")
    else:
    # Если ответ неверный, проверяем, находится ли игрок в комнате 'trap_room'
        if current_room == 'trap_room':
            # Вызываем функцию trigger_trap
            trigger_trap(game_state)
        else:
            print("Неправильно. Попробуйте ещё раз.")

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

def show_help():
    """
    Выводит список доступных команд и их описание.
    """
    print("\nДоступные команды:")
    # Перебираем все команды и их описания
    for command, description in COMMANDS.items():
        # Позиционируем описание с отступом 16 пробелов
        print(f" {command.ljust(16)} - {description}")

def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное целое число в диапазоне [0, modulo).
    :param seed: Целое число (например, количество шагов).
    :param modulo: Целое число (диапазон результата).
    :return: Целое число в диапазоне [0, modulo).
    """
    # Возьмите синус от seed, умноженного на большое число с дробной частью
    # Например, 12.9898 — это большое число с дробной частью
    sin_value = math.sin(seed * 12.9898)
    
    # Результат умножьте на другое большое число с дробной частью
    # Например, 43758.5453 — это большое число с дробной частью
    scaled_value = sin_value * 43758.5453
    
    # От полученного числа нам нужна только его дробная часть
    # Простой способ получить дробную часть — вычесть из числа его целую часть
    fractional_part = scaled_value - math.floor(scaled_value)
    
    # Умножьте эту дробную часть на modulo, чтобы привести значение к нужному диапазону [0, modulo)
    result = fractional_part * modulo
    
    # Отбросьте дробную часть и верните целое число
    return int(result)

def trigger_trap(game_state):
    """
    Имитирует срабатывание ловушки и приводит к негативным последствиям для игрока.
    :param game_state: Словарь состояния игры.
    """
    # Выводим сообщение о том, что ловушка активирована
    print("Ловушка активирована! Пол стал дрожать...")

    # Получаем инвентарь игрока
    inventory = game_state['player_inventory']

    # Проверяем, есть ли у игрока предметы в инвентаре
    if inventory:
        # Если инвентарь не пуст, используем функцию pseudo_random для 
        # выбора случайного индекса предмета
        # В качестве seed используем количество шагов игрока
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        # Удаляем предмет по выбранному индексу
        lost_item = inventory.pop(index)
        # Сообщаем игроку, какой предмет он потерял
        print(f"Вы потеряли: {lost_item}")
    else:
        # Если инвентарь пуст, генерируем случайное число от 0 до 9
               # Генерируем случайное число в диапазоне [0, 10)
        damage = pseudo_random(game_state['steps_taken'], len(inventory))
        # Проверяем, меньше ли число определённого порога (3)
        if damage < 3:
            # Если число меньше порога, игра заканчивается (игрок проиграл)
            print("Вы получили урон! Игра окончена.")
            game_state['game_over'] = True
        else:
            # Если число больше или равно порогу, игрок уцелел
            print("Вы уцелели! Ловушка не причинила вам вреда.")

def random_event(game_state):
    """
    Генерирует случайное событие при перемещении игрока.
    :param game_state: Словарь состояния игры.
    """
    # Сначала определяем, произойдет ли событие вообще
    # Используем pseudo_random с модулем 10, чтобы получить число от 0 до 9
    # Если результат равен 0, событие происходит (вероятность 1/10 = 10%)
    event_chance = pseudo_random(game_state['steps_taken'], 10)
    
    # Проверяем, произошло ли событие
    if event_chance != 0:
        # Если событие не произошло, выходим из функции
        return
    
    # Если событие произошло, выбираем, какое именно событие случится
    # Используем pseudo_random с модулем 3, чтобы получить число от 0 до 2
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)  
    # +1, чтобы получить другой результат
    
    # Сценарий 1: Находка (игрок находит монету)
    if event_type == 0:
        print("Вы нашли монету на полу!")
        # Добавляем 'coin' в список предметов текущей комнаты
        current_room = game_state['current_room']
        room_items = get_room_items(current_room)
        room_items.append('coin')
    
    # Сценарий 2: Испуг (игрок слышит шорох)
    elif event_type == 1:
        print("Вы слышите шорох за спиной...")
        # Проверяем, есть ли у игрока в инвентаре 'sword'
        if 'sword' in game_state['player_inventory']:
            print("Вы достали меч. Шорох стих.")
        else:
            print("Вы испугались и отступили назад.")
    
    # Сценарий 3: Срабатывание ловушки
    elif event_type == 2:
        current_room = game_state['current_room']
        # Проверяем, находится ли игрок в комнате 'trap_room'
        if current_room == 'trap_room':
            # Проверяем, есть ли у игрока в инвентаре 'torch'
            if 'torch' in game_state['player_inventory']:
                print("Вы включили факел и заметили ловушку. Удачно избежали!")
            else:
                print("Ловушка сработала!")
                # Вызываем функцию trigger_trap
                trigger_trap(game_state)