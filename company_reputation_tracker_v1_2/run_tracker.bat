@echo off
call venv\Scripts\activate
set PYTHONPATH=%CD%
python reputation_tracker\main.py run
pause