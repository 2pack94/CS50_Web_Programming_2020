video: https://www.youtube.com/watch?v=w8q0C-C1js4&feature=youtu.be
notes: https://cs50.harvard.edu/web/2020/notes/3/
source code: http://cdn.cs50.net/web/2020/spring/lectures/3/src3.zip
assignment: https://cs50.harvard.edu/web/2020/projects/1/wiki/

This lecture is about the basics of the Django Framework
Django documentation: https://docs.djangoproject.com/en/3.1/
Django Tutorial: https://docs.djangoproject.com/en/3.1/intro/tutorial01/

Getting Started:
    # create a virtual environment with pipenv and install django
    (venv) $ pipenv install django

    # create a django project
    (venv) $ django-admin startproject lecture_project

    # create an app (a module of the project)
    (venv) $ python3 manage.py startapp lecture_app

    # start the server
    (venv) $ python3 manage.py runserver

    # the server is reachable on the following address: http://127.0.0.1:8000/

URL dispatcher: https://docs.djangoproject.com/en/3.1/topics/http/urls/
    The URL dispatcher routes URLs to views

Templates: https://docs.djangoproject.com/en/3.1/topics/templates/
    Templates are a way to generate HTML dynamically
    By default Django uses its own templating language
    It supports variables, if statements, loops, Template inheritance, ...

Forms: https://docs.djangoproject.com/en/3.1/topics/forms/
    Django provides tools and libraries to build HTML forms
    By default Django uses middleware that checks the CSRF token when posting a form

Sessions: https://docs.djangoproject.com/en/3.1/topics/http/sessions/
    A session stores data that is associated to a user that visits the Web site.
    By default, Django stores session data in the database.
