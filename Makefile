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


# Команда для проверки кода
lint:
	poetry run ruff check .

# Команда для автоматического исправления ошибок
lint-fix:
	poetry run ruff check . --fix