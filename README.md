`pip install -r requirements.txt`
touch .env
FLASK_DEBUG=1
FLASK_APP=data_engineering.common.application:get_or_create()
`mkdir app`
`touch app/application.py`
(see `app/application.py`)
`mkdir -p app/config`
`touch app/config/defaults.yml`
(see `app/config/defaults.yml`)
mkdir app/api
touch app/api/routes.py
touch app/api/views.py
mkdir app/commands
touch app/commands/__init__.py
touch app/commands/dev.py
touch manage.py
# create database postgresql://postgres@localhost/data-engineering-sample-app
# add a hawk user: insert into
create database and tables: `python manage.py dev db --create`
create hawk user: `python manage.py dev add_hawk_user --client_id client_id1 --client_key client_key1 --client_scope '*' --description user1`
make sure redis server is running
