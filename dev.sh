#!/bin/bash
source venv/bin/activate
watchmedo auto-restart --pattern="*.py" --recursive --directory="." python3 main.py