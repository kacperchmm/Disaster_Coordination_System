# Makefile

PYTHON=python
MAIN=src/main.py

run:
	@PYTHONPATH=src $(PYTHON) $(MAIN)

clean:
	@find . -name '*.pyc' -delete

help:
	@echo "Usage:"
	@echo "  make run    - Run the main script"
	@echo "  make clean  - Remove .pyc files"
	@echo "  make help   - Show this help message"
