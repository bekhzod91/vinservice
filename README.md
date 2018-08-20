### Install
```
$ git clone https://github.com/myrubapa/vinservice
$ cd vinservice
$ docker-compose build
```

### Run test
```
$ docker-compose -f docker-compose.test.yml run web
```

### Run app
```
$ docker-compose up -d
$ # Wait some time for app run
$ chrome http://localhost:8000/
```

### Fetch vehicle data 
```
curl -s http://localhost:8000/vehicle/KMHDU4ADXAU832403/vin/ | python -m json.tool
```

#### Create admin
```
$ docker-compose up -d
$ # Wait some time for app run
$ docker-compose run --entrypoint="/bin/bash" web
$ source .venv/bin/activate
$ python manage.py createsuperuser
$ exit
$ chrome http://localhost:8000/admin/
```
