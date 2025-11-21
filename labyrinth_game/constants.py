# labyrinth_game/constants.py
# Словарь ROOMS: ключ — название комнаты, значение — словарь с её свойствами

ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. На полу лежит старый факел.',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с cундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': ('Назовите число, после 9". Введите ответ цифрой или словом.', '10')
    },
    'trap_room': {
          'description': 'Комната yа стене видна надпись: "Осторожно — ловушка".',
          'exits': {'west': 'entrance'},
          'items': ['rusty_key'],
          'puzzle': ('Назовите слово "шаг" (введите "шаг")', 'шаг')
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки.',
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient_book'],
          'puzzle': ('Что растет, когда его съедают?" (ответ одно слово)', 'резонанс')  
    },
        'armory': {
          'description': 'Старая оружейная комната. На стене висит меч, шкатулка.',
          'exits': {'south': 'library'},
          'items': ['sword', 'bronze_box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': 'Комната, на столе сундук. Дверь заперта нужен особый ключ.',
          'exits': {'south': 'hall'},
          'items': ['treasure_chest'],
          'puzzle': ('Введите код (подсказка: 2*5= ? )', '10')
    }
    # ... добавьте сюда остальные комнаты
}

# Словарь COMMANDS: ключ — команда, значение — описание
COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}

# Глобальная переменная для хранения
TREASURE_CODE = '10'# Правильный код для открытия сундука