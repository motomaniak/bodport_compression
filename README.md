## Setup
To run this project, you'll need to install redis


open a terminal and start redis server
```
$ redis-server
```

After installing redis server open another terminal 

```
$ cd file_compressor
$ source venv/bin/activate
$ python manage.py runserver
```

Open a third terminal
```
$ cd file_compressor
$ source venv/bin/activate
$ celery -A file_compressor worker -l INFO

```
