# project 4: **SuShee Fashionista**

Web Programming with Python and JavaScript

This application was developed using Python Django, HTML, Javascript and CSS.
This web page allows the users to register / login and order your favorite clothe designs online. User can also rate and review clothes once logged in. Users can add items to cart and pay using their credit cards. The django admin user is able to add / delete items from the shopping list.

## Download

``` bash
git clone https://github.com/firaan1/susheefashionista.git
```

## Start **SuShee Fashionista**
In order to setup the database, import data and start this app for the first time, please follow the instructions below,
``` bash
# Install required python packages from requirements.txt file
pip install -r requirements.txt
# create database tables using django
python manage.py makemigrations
python manage.py migrate
# input data into database
python manage.py shell < prep.py
# create admin user with your own username and password to access admin page
python manage.py createsuperuser
# start django server
python manage.py runserver
```
