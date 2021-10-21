# Team Fast Backend
This project's goal is to create a framework that has been designed to efficiently route delivery drivers coming from a single location. It also provides an easy-to-use interface (on the frontend) for managers that create routes, as well as the drivers that deliver using those routes. 

## Milestone 1: Release Notes
Many of the backend features are currently still in development. Right now all of the models are working in the database and we have begun work on the serializers and views. The serializers will be able to transform python objects to JSON and vice versa. The views will handle our API routes and the type of request (get, post, put, etc.).

Currently, our only working API route is `/locations/`

## Milestone 2: Release Notes

* Routing algorithm:

* Backend:

# Installation
## Install and update Python

## Create a virtual environment
`python3 -m venv venv`

### For windows:
`python -m venv venv`

## Start virtual environment
### For linux/mac/git bash
`. venv/bin/activate`

### For windows:
`venv\Scripts\activate`

## Install/Upgrade pip
`python -m pip install --upgrade pip`

## Install packages
`pip install -r requirements.txt`

## Download/Install Postgres
https://www.postgresql.org/download/

### Create database
`psql -U postgres`
Then enter in your password. (You may have to add postgres to your path variable)

Create the database
`CREATE DATABASE fastDB;` you can then quit with `exit;`

## Copy settings
`cp backend/settings.example backend/settings.py`

Change password in `settings.py` to same password used in Postgres installation

## Make Migrations
`python manage.py makemigrations backend`

Then

`python manage.py migrate backend`

## Create superuser
`python manage.py createsuperuser`

May have to use `winpty python manage.py createsuperuser`
