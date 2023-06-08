# Test Assignment for QA
Repository for demonstrating the execution of a test task in the company N

### Preparing to launch autotests
1. Install requirements
```
pip install -r requirements.txt
```
2. Done

### Run autotests
**Only in console**
```
pytest
```

**With UI-report**
1. Install Allure (use [documentation](https://docs.qameta.io/allure-report/#_about) to install if you're using something else than MacOS)
```
brew install allure 
```
2. Run autotests
```
pytest --alluredir=./reports/allure
```
3. Open report in browser 
```
allure serve ./reports/allure
```