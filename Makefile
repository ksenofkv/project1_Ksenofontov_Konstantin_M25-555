# Makefile

# Команда для установки зависимостей
install:
	poetry install

# Команда для запуска проекта
project:
	poetry run project

# Команда для создания дистрибутива (если нужно)
dist:
	poetry build

# Команда для очистки (опционально)
clean:
	rm -rf .venv/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

# Команда для проверки стиля кода (если используется линтер)
lint:
	poetry run flake8 labyrinth_game/

# Команда для запуска тестов (если есть)
test:
	poetry run pytest tests/


# Команда для сборки пакета
build:
	poetry build

# Команда для публикации пакета
publish:
	poetry publish --dry-run

# Команда для установки собранного пакета из директории dist/
package-install:
	python3 -m pip install dist/*.whl