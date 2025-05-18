## Install

Install dependencies
```
pip install -r requirements.txt
```

Run migrations to initialize database tables:
```
python manage.py migrate
```

Create super-user for the admin:
```
python manage.py createsuperuser
```
## Run
```
python manage.py runserver
```

The map visible at [http://127.0.0.1:8000](http://127.0.0.1:8000) can be edited from the admin site at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).