# labyrinth_game/player_actions.py

from labyrinth_game.utils import get_room_exits, describe_current_room, get_room_items, get_room_puzzle 
# Импортируем необходимые функции из utils.py

def show_inventory(game_state):
    """
    Отображает инвентарь игрока.
    :param game_state: Словарь состояния игры.
    """
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ', '.join(inventory))
    else:
        print("Инвентарь пуст.")
   
def get_input(prompt="> "):
    """
    Запрашивает ввод пользователя.
    :param prompt: Текст приглашения.
    :return: Введённая строка или "quit" при прерывании.
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
def move_player(game_state, direction):
    """
    Перемещает игрока в указанном направлении.
    :param game_state: Словарь состояния игры.
    :param direction: Направление (например, 'north').
    """
    # Получаем текущую комнату из состояния игры
    current_room = game_state['current_room']
    
    # Получаем словарь выходов для текущей комнаты
    exits = get_room_exits(current_room)
    
    # Проверяем, существует ли выход в указанном направлении
    if direction in exits:
        # Если выход есть, получаем название новой комнаты
        new_room = exits[direction]
        
        # Проверяем, является ли новая комната 'treasure_room'
        if new_room == 'treasure_room':
            # Проверяем, есть ли у игрока ключ 'rusty_key' в инвентаре
            if 'rusty_key' in game_state['player_inventory']:
                # Если ключ есть, разрешаем переход
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
                # Обновляем текущую комнату
                game_state['current_room'] = new_room
                # Увеличиваем количество шагов
                game_state['steps_taken'] += 1
                # Выводим описание новой комнаты
                print(f"Вы переместились в {new_room}.")
            else:
                # Если ключа нет, выводим сообщение и не разрешаем переход
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        else:
            # Если новая комната не 'treasure_room', разрешаем переход
            # Обновляем текущую комнату
            game_state['current_room'] = new_room
            # Увеличиваем количество шагов
            game_state['steps_taken'] += 1
            # Выводим описание новой комнаты
            print(f"Вы переместились в {new_room}.")
    else:
        # Если выхода нет, выводим сообщение об ошибке
        print(f"Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    """
    Позволяет игроку взять предмет из комнаты.
    :param game_state: Словарь состояния игры.
    :param item_name: Название предмета.
    """
    # Получаем текущую комнату из состояния игры
    current_room = game_state['current_room']
    
    # Получаем список предметов в текущей комнате
    room_items = get_room_items(current_room)
    
    # Проверяем, есть ли предмет в комнате
    if item_name in room_items:
        # Проверяем, является ли предмет 'treasure_chest'
        if item_name == 'treasure_chest':
            # Если да, выводим сообщение, что сундук слишком тяжёлый
            print("Вы не можете поднять сундук, он слишком тяжёлый.")
            return  # Выходим из функции, не добавляя предмет в инвентарь

        # Добавляем предмет в инвентарь игрока
        game_state['player_inventory'].append(item_name)
        # Удаляем предмет из списка предметов комнаты
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """
    Позволяет игроку использовать предмет из инвентаря.
    :param game_state: Словарь состояния игры.
    :param item_name: Название предмета.
    """
    inventory = game_state['player_inventory']

    # Проверяем, есть ли предмет в инвентаре
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    # Выполняем уникальное действие для каждого предмета
    if item_name == 'torch':
        print("Вы зажгли факел. Теперь вы видите больше деталей в темноте.")
    elif item_name == 'sword':
        print("Вы вытащили меч. Он блестит в свете факела.")
    elif item_name == 'bronze_box':
        print("Вы открыли бронзовую коробку. Внутри лежит ржавый ключ.")
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Вы добавили 'rusty_key' в свой инвентарь.")
    elif item_name == 'rusty_key':
        print("Вы вставили ржавый ключ в замок. Замок щёлкнул!")
    else:
        print("Игрок не знает, как использовать этот предмет.")


