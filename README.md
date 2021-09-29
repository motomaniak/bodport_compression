## Setup
To run this project, you'll need to install redis


open a terminal and start redis server

```
$ redis-server
```

Open a second terminal to start server

```
$ cd file_compressor
$ source venv/bin/activate
$ cd file_compressor
$ python manage.py runserver
```

Open a third terminal to start celery
```
$ cd file_compressor
$ source venv/bin/activate
$ cd file_compressor
$ celery -A file_compressor worker -l INFO

```
