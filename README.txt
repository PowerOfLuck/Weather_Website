Клонируйте репозиторий:
git clone https://github.com/PowerOfLuck/Weather_Website.git

Перейдите в терминале в папку с репозиторием

Убедитесь, что у вас установлен Docker.

### Запуск

Запустите контейнеры:
docker-compose up --build

Примените миграции базы данных:
docker-compose exec web python manage.py migrate



*********************************************************************
### Если у вас по каким-то причинам не удалось запустить с Docker, то:

a) Скачайте предыдущий коммит по ссылке 
https://github.com/PowerOfLuck/Weather_Website/tree/bb790caec1ade504344ea5c2da3ca0c821704555 

b) Ручной откат 

Создайте виртуальное окружение
Shift + Right click;
"Открыть Power Shell здесь";
python -m venv venv;

Установите зависимости из requirements.txt

в фаиле в строчке 
"DATABASE_HOST=db" 
замените на 
"DATABASE_HOST=localhost"

В терминале вашего редактора активируйте созданное Вами виртуальное окружение 
с зависимостями, и введите эти три строчки:

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

Сервер станет доступен по адресу http://127.0.0.1:8000/
*********************************************************************


