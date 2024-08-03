# Modern-Application-Development-II-Project-IITM-Sponsify


#terminal 1
sudo apt update
sudo apt install redis-server
sudo nano /etc/redis/redis.conf			(change "supervised no" to "supervised system" for ubuntu)
sudo service redis-server restart


#terminal 2
. ./.venv/bin/activate
cd backend
celery -A make_celery.celery_app worker --loglevel INFO


#terminal 3
. ./.venv/bin/activate
cd backend
celery -A make_celery.celery_app beat


#terminal 4
. ./.venv/bin/activate
cd backend
python main.py


#terminal 5
cd frontend/sponsify
npm run serve

