export UV_SKIP_WHEEL_FILENAME_CHECK := 1

run:
	uv run -m src

install:
	uv add ./mazegenerator-00001-py3-none-any.whl
	uv sync

clean:
	@uv run -m pyclean . --debris
	@rm -rf .mypy_cache
	@echo "\e[42m\e[30m Directory is cleaned \e[0m"

lint:
	-python3 -m flake8 . --exclude=.venv
	-python3 -m mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs
