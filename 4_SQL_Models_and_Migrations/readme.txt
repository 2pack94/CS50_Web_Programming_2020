video: https://www.youtube.com/watch?v=YzP164YANAU
notes: https://cs50.harvard.edu/web/2020/notes/4/
source code: cdn.cs50.net/web/2020/spring/lectures/4/src4.zip
assignment: https://cs50.harvard.edu/web/2020/projects/2/commerce/

SQL:
    Django uses SQLite as its default database implementation. SQLite is very lightweight and stores the data in a single database file.

Django Models: https://docs.djangoproject.com/en/3.1/topics/db/models/
    Django Models are an abstraction layer on top of the database.
    A Model is a Python class that represents a table inside the database. Each class member represents a column in a database table.
    Django will generate SQL commands to interact with the database when corresponding methods of the Model class are called (e.g. save()).
    Using Models removes the risk of SQL injection.
    
    Migrations:
        Migrations are changes (instructions for Django) to the database according to the created Django Models.
        When migrating, the Migrations get applied to the database. The database tables get created/ updated.

        # Create Migrations. Needed every time a Model (inside models.py) has changed
        $ python3 manage.py makemigrations

        # Apply Migrations.
        $ python3 manage.py migrate

Django admin app: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
    Web Interface designed to view and modify Models.
    The Models must be registered inside admin.py first.
    Can be accessed via http://127.0.0.1:8000/admin/
    # create a superuser inside the database to get access to the django admin site
    # (use username and password: admin, admin)
    $ python3 manage.py createsuperuser

Django users: https://docs.djangoproject.com/en/3.1/topics/auth/
    Users can be added inside the admin site or inside Django with the create_user() helper function.

session-based Authentication:
    After the user logs in, a session is generated and the session ID is stored in a cookie.
    The browser stores the cookie, which gets sent anytime a request is made to the server.
    Django uses sessions and middleware to hook the authentication system into request objects.
    These provide a request.user attribute on every request which represents the current user.
