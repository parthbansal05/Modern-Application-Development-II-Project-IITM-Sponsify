# Modern-Application-Development-II-Project-IITM-Sponsify

## Terminal 1
sudo apt update <br>
sudo apt install redis-server <br>
sudo nano /etc/redis/redis.conf			(change "supervised no" to "supervised system" for ubuntu) <br>
sudo service redis-server restart <br>
<br>

## Terminal 2
. ./.venv/bin/activate <br>
cd backend <br>
celery -A make_celery.celery_app worker --loglevel INFO <br>
<br>

## Terminal 3
. ./.venv/bin/activate <br>
cd backend <br>
celery -A make_celery.celery_app beat <br>
<br>

## Terminal 4
. ./.venv/bin/activate <br>
cd backend <br>
python main.py <br>
<br>

## Terminal 5
cd frontend/sponsify <br>
npm run serve <br>

