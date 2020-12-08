# bfg.com

```bash
apt-get install python3  python3-dev build-essential libssl-dev \
    libffi-dev libxml2-dev libxslt1-dev zlib1g-dev lib-pq python3-virtualenv
```

```
virtualenv -p python3 venv
```

```
. ./venv/bin/activate
```

```
pip install -r requirements.txt
```

```
cd bfg
./manage.py migrate
./manage.py runserver 8000
````
