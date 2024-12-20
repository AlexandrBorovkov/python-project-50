install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

package-reinstall:
	python3 -m pip install --force-reinstall dist/*.whl

gendiff:
	poetry run gendiff

lint:
	poetry run ruff check

test:
	poetry run pytest -v

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint