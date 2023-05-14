# ConviousQATask
Repository for demonstrating the execution of a test task in the company Convious

### Preparing to launch autotests
1. Install requirements
- ```pip install -r requirements.txt```
2. Done

### Run autotests
With HTML-report (will be available in /test/reports)
```
pytest --html-report=./tests/reports
```
With marks
```
pytest -v -m <MARK_NAME>
```
Only in console
```
pytest
```