SHELL := /bin/zsh

BACKEND_DIR := backend
FRONTEND_DIR := frontend
VENV_DIR := $(BACKEND_DIR)/.venv
VENV_BIN := $(abspath $(VENV_DIR))/bin
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
UVICORN := $(VENV_BIN)/uvicorn
NPM := npm

.PHONY: help backend-venv backend-install backend-run backend-db-check frontend-install frontend-run install dev

help:
	@echo "Available targets:"
	@echo "  make backend-install   Create Python venv and install backend dependencies"
	@echo "  make backend-run       Run FastAPI on http://127.0.0.1:8000"
	@echo "  make backend-db-check  Run PostgreSQL connection stub"
	@echo "  make frontend-install  Install frontend dependencies"
	@echo "  make frontend-run      Run Vite on http://localhost:5173"
	@echo "  make install           Install backend and frontend dependencies"
	@echo "  make dev               Run backend and frontend together"

backend-venv:
	python3 -m venv $(VENV_DIR)

backend-install: backend-venv
	$(PIP) install -r $(BACKEND_DIR)/requirements.txt

backend-run:
	cd $(BACKEND_DIR) && $(UVICORN) app.main:app --reload

backend-db-check:
	cd $(BACKEND_DIR) && $(PYTHON) app/database/main.py

frontend-install:
	cd $(FRONTEND_DIR) && $(NPM) install

frontend-run:
	cd $(FRONTEND_DIR) && $(NPM) run dev

install: backend-install frontend-install

dev:
	@trap 'kill 0' EXIT; \
	$(MAKE) backend-run & \
	$(MAKE) frontend-run & \
	wait
