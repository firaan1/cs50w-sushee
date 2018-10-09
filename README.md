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

## Contents

The directory structure is shown below,

``` bash
susheefashionista/
├── db.sqlite3 # database (will be created by the admin from the command line using migration)
├── manage.py # django file
├── media # media folder where uploaded files are saved
│   └── documents
├── prep # prep folder containing images which will be imported into the database by prep.py file
├── prep.py # preparation file to import data into database
├── README.md # readme
├── requirements.txt # python package requirements. must be installed using pip
├── shopping # django app folder
│   ├── admin.py # admin site difinitions
│   ├── apps.py
│   ├── forms.py # forms containing function to upload data
│   ├── __init__.py
│   ├── migrations
│   ├── models.py # containing all the database models used
│   ├── __pycache__
│   ├── static
│   │   └── shopping
│   │       ├── css
│   │       │   └── mystyle.css # included style sheet file
│   │       └── images # used images
│   │           ├── img1.jpg
│   │           ├── img2.jpg
│   │           ├── img3.jpg
│   │           ├── img4.jpg
│   │           └── img.jpg
│   ├── templates # html templates
│   │   └── shopping
│   │       ├── additems.html # allows admin to add items to the database
│   │       ├── cart.html
│   │       ├── collections.html # shows all the dress collections
│   │       ├── dressitem.html # individual dress page
│   │       ├── histories.html # contains order histories
│   │       ├── index.html # home page
│   │       ├── layout.html # base layout for all other html files
│   │       ├── login.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py # containing url definitions
│   └── views.py # contains python function definitions for django
└── sushee
    ├── __init__.py
    ├── __pycache__
    ├── settings.py # django settings file where the app, static and media folders are registered
    ├── urls.py
    └── wsgi.py
```
