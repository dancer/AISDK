#!/bin/bash
source venv/bin/activate
watchmedo auto-restart --pattern="*.py" --recursive --directory="." python main.py