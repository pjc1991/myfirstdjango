# 마이 퍼스트 장고

장고를 이용한 간단한 웹 어플리케이션 구현.
간단한 CMS 구현을 목표로 한다.

## 프로젝트 시동


```{python}
# initialize of venv
python3 -m venv ./venv && source ./venv/bin/activate && pip install -r requirements.txt

# execution
source ./venv/bin/activate
python manage.py runserver

# quit
control + c
deactivate
```