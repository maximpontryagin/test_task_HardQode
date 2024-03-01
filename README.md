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

**Примеры запросов и ответов.**
- **_Опубликовать отзыв:**_


- **_Список доступных для покупки продуктов._**
_GET запрос на http://127.0.0.1:8000/api/v1/available_products/_
**_Ответ:_**
[
    {
        "id": 13,
        "author": "admin",
        "num_lessons": 2,
        "title": "Python backend developer",
        "start_datetime": "2024-02-29T21:18:47.437272+03:00",
        "price": "999.00",
        "max_users_in_group": 16,
        "min_users_in_group": 5
    }
]

- **_Выделение списка уроков по конкретному продукту к которому пользователь имеет доступ:_**
_GET запрос на http://127.0.0.1:8000/api/v1/user_lessons/{product_id}/_
**_Ответ:_**
[
    {
        "id": 3,
        "title": "Первый урок python разработчик",
        "video_url": "https://www.youtube.com/",
        "product": 1
    }
]
- **_отображения списка всех продуктов на платформе с дополнительными полями (доп задание)._**
_GET запрос на http://127.0.0.1:8000/api/v1/products/_
**_Ответ:_**
[
    {
        "id": 1,
        "num_students": 19,
        "group_fill_percentage": 100.0,
        "product_purchase_percentage": 90.47619047619048,
        "title": "Python разработчик",
        "start_datetime": "2024-02-29T16:51:47.946805+03:00",
        "price": "100.00",
        "max_users_in_group": 10,
        "min_users_in_group": 5,
        "author": 1
    }
]

- **_Покупака продукта и получаение к нему доступа. После этого пользователя распределяет в учебную группу продукта._**
_POST запрос на http://127.0.0.1:8000/api/v1/buy/_
**_В теле запроса указать id желаего к покупке продукта:_**
{
    "product": 1
}

**_Ответ:_**
{
    "product": 1
}