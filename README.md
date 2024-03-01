**Описание.**
Проект school_project это проект, для онлайн школы. В ней присутсвуют продукты, группы и уроки. В данном проекте представлен backend school_project.

**Стек используемых технологий.**
* Django 4.2
* sqlite3 
* python 3.11.3

**Как развернуть проект.**
1. Клонировать репозиторий и перейти в него в командной строке:
_git clone git@github.com:maximpontryagin/test_task_HardQode.git cd school_project_

2. Cоздать и активировать виртуальное окружение:
_python -m venv venv source venv/Scripts/activate_ 

3. Установить зависимости из файла requirements.txt:
_pip install -r requirements.txt_ 

4. Выполнить миграции:
_python manage.py migrate_

5. Запустить проект:
_python manage.py runserver_