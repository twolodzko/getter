
dist: getter
	pip install build
	python -m build

.PHONY: install
install: dist
	pip install --force-reinstall dist/*.whl

.PHONY: allchecks
allchecks: stylecheck typecheck test

.PHONY: test
test:
	pytest -v --color=yes --doctest-modules .

.PHONY: typecheck
typecheck:
	mypy --ignore-missing-imports .

.PHONY: stylefix
stylefix:
	isort --settings-path pyproject.toml .
	black --config pyproject.toml .

.PHONY: stylecheck
stylecheck:
	isort --settings-path pyproject.toml --check .
	black --config pyproject.toml --check .

.PHONY: clean
clean:
	rm -rf ./dist getter.egg-info .mypy_cache .pytest_cache __pycache__
