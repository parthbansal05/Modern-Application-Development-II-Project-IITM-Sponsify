# Modern-Application-Development-II-Project-IITM-Sponsify

The project is designed to run on Ubuntu

# Initlize the project 
```
run `python -m venv venv` to create a virtual environment
run `source venv/bin/activate` to activate the virtual environment
run `pip install -r requirements.txt` to install the required packages
run `python init.py` to initialize the project
```


# Run the project

## Terminal 1
```
sudo apt update
sudo apt install redis-server
sudo nano /etc/redis/redis.conf			(change "supervised no" to "supervised system" for ubuntu)
sudo service redis-server restart
```

## Terminal 2
```
. ./.venv/bin/activate
cd backend
celery -A make_celery.celery_app worker --loglevel INFO
```

## Terminal 3
```
. ./.venv/bin/activate
cd backend
celery -A make_celery.celery_app beat
```

## Terminal 4
```
. ./.venv/bin/activate
cd backend
python main.py
```

## Terminal 5
```
cd frontend/sponsify
npm run serve
```
