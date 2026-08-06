run:
	uv run -m src

install:
	uv sync

clean:
	@uv run -m pyclean . --debris
	@rm -rf .mypy_cache
	@echo "\e[42m\e[30m Directory is cleaned \e[0m"

lint:
	-uv run ruff check .
	-uv run ruff format --check .
	-python3 -m mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

