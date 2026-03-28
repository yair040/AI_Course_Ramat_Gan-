# Makefile — AutoEncoder project
# Author: Yair Levi
# Run from project root (AutoEncoder/)

VENV        := ../../venv
PYTHON      := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
PYTEST      := $(VENV)/bin/pytest

.PHONY: help setup install test run-all run-1 run-2 run-3 run-4 run-5 clean logs

help:
	@echo ""
	@echo "AutoEncoder — available targets:"
	@echo "  make setup       Create venv and install dependencies"
	@echo "  make install     Install package in editable mode"
	@echo "  make test        Run smoke tests"
	@echo "  make run-1       Task 1: preprocess images"
	@echo "  make run-2       Task 2: train cats autoencoder"
	@echo "  make run-3       Task 3: train dogs autoencoder"
	@echo "  make run-4       Task 4: cats-enc + dogs-dec"
	@echo "  make run-5       Task 5: dogs-enc + cats-dec"
	@echo "  make run-all     Run all tasks in order"
	@echo "  make logs        Tail the latest log file"
	@echo "  make clean       Remove output/ and log/"
	@echo ""

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Venv ready at $(VENV)"

install:
	$(PIP) install -e .

test:
	$(PYTEST) tests/ -v

run-1:
	$(PYTHON) tasks.py --task 1

run-2:
	$(PYTHON) tasks.py --task 2

run-3:
	$(PYTHON) tasks.py --task 3

run-4:
	$(PYTHON) tasks.py --task 4

run-5:
	$(PYTHON) tasks.py --task 5

run-all:
	$(PYTHON) tasks.py --task all

logs:
	tail -f log/autoencoder.log

clean:
	rm -rf output/ log/
	@echo "Cleaned output/ and log/"
