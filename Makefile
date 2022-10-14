SHELL := /bin/bash

DC=docker-compose
FM=black
IM=isort

up:
	- $(DC) up --build --detach

build:
	- $(DC) build

down:
	- $(DC) down

format:
	- $(IM) .
	- $(FM) .
