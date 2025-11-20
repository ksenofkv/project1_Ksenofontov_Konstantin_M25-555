#!/usr/bin/env python3

#def main():
#    print("Первая попытка запустить проект!")

#if __name__ == "__main__":
#    main()


from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import move_player, look_around, show_inventory, get_input, take_item, use_item
from labyrinth_game.utils import describe_current_room, attempt_open_treasure, solve_puzzle, show_help

# --- Определение состояния игры ---
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значение окончания игры
    'steps_taken': 0  # Количество шагов
}

def main():
    """
    Главная функция игры.
    Управляет игровым циклом.
    """
    print("Добро пожаловать в Лабиринт сокровищ!")
    current_room = game_state['current_room']
    inventory = game_state['player_inventory']

    while not game_state['game_over']:
        print("\n---")
        describe_current_room(game_state)

        # Получаем команду от игрока
        command = get_input("Введите команду (look, go, take, use, inventory, solve, help, quit): ").strip()

        # Обрабатываем команду
        process_command(game_state, command)

        attempt_open_treasure(game_state)        

    print(f"Вы прошли {game_state['steps_taken']} шагов.")



def process_command(game_state, command):
    """
    Обрабатывает команду, введенную пользователем.
    :param game_state: Словарь состояния игры.
    :param command: Команда, введенная пользователем.
    """
    # Разделяем команду на части
    parts = command.split()
    if not parts:
        return

    # Определяем команду и аргумент
    cmd = parts[0].lower()
    arg = ' '.join(parts[1:]) if len(parts) > 1 else None

    # Обрабатываем команду
    match cmd:
        case 'look':
            # Вызываем функцию описания текущей комнаты
            describe_current_room(game_state)
        case 'go':
            # Проверяем, есть ли аргумент (направление)
            if arg:
                # Вызываем функцию перемещения игрока
                move_player(game_state, arg)
            else:
                # Если аргумента нет, выводим сообщение
                print("Укажите направление (например, 'go north').")
        case 'take':
            # Проверяем, есть ли аргумент (название предмета)
            if arg:
                # Вызываем функцию взятия предмета
                take_item(game_state, arg)
            else:
                # Если аргумента нет, выводим сообщение
                print("Укажите предмет (например, 'take torch').")
        case 'use':
            # Проверяем, есть ли аргумент (название предмета)
            if arg:
                # Вызываем функцию использования предмета
                use_item(game_state, arg)
            else:
                # Если аргумента нет, выводим сообщение
                print("Укажите предмет (например, 'use torch').")
        case 'inventory':
            # Вызываем функцию отображения инвентаря
            show_inventory(game_state)
        case 'solve':
            # Вызываем функцию решения загадки
            solve_puzzle(game_state)
        case 'help':
            # Вызываем функцию показа помощи
            show_help()
        case 'quit':
            # Выводим сообщение и завершаем игру
            print("Спасибо за игру!")
            game_state['game_over'] = True
        case _:
            # Если команда не распознана, выводим сообщение
            print("Неизвестная команда. Попробуйте: look, go, take, use, inventory, solve, help, quit.")



if __name__ == "__main__":
    main()