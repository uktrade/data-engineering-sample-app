# Data Engineering Sample App
A minimal example of how to use the [data-engineering-common](https://github.com/uktrade/data-engineering-common/) repository to create a lightweight Flask, hawk authenticated app.

## Installation
This installation is set up for installing on `localhost`, for a Docker workflow see the examples of other apps based on `data-engineering-common` below.

1. Clone repository
2. Create a python virtual environment, e.g. if using [virtualenv](https://virtualenv.pypa.io/en/stable/index.html) `virtualenv venv`
3. Activate the virtualenv, e.g. `source venv/bin/activate`
4. Install python libraries, `pip install -r requirements.txt`
5. Configure the app database connection, `app/config/defaults.yml database_url`
6. Configure the app cache connection, `app/config/defaults.yml cache:*`
7. Install postgres and redis if not already installed
8. Create app database and tables, `python manage.py dev db --create`
9. Create a hawk user: `python manage.py dev add_hawk_user --client_id client_id1 --client_key client_key1 --client_scope '*' --description user1`
10. Run the application server, `flask run`

Note: The `requirements.txt` file includes a reference to the `data-engineering-common` repo, if a newer version of the repo is released you may need to manually uninstall the old version before reinstalling the newer version. `pip remove data-engineering-common`.

## Files
`app/`: basically where all the app logic lives
`app/api`: api logic, routes and views essentially
`app/api/routes.py`: The list of urls that make up the api and their corresponding views. There are 3 routes here,
* /get-data: an unauthenticated route
* /get-data-authenticated: a hawk authenticated route
* /train-model: a route to trigger some process on the app server
* additional routes are also inherited from the `data-engineering-common` repo, e.g. /healthcheck which is used by Cloud Foundry to periodically check whether the app server is running without any issues
`app/api/views.py`: Here lies the python implementations of the api routes. `get_data` is a fairly simple view. `get_data_authenticated` showcases how to write a hawk authenticated view, it does this by using several decorators, `json_error` is for making any errors more meaningful, `response_orientation_decorator` is used for managing the data structure of the returned data, there are two options, `tabular` and `records` (inspired by pandas dataframes and their `to_dict` method). `tabular` will return the data in the form, {'headers': ['header1', 'header2'], 'values': [('value1', 'value2'), ('value3', 'value4'), ...]}, `records` will return data in json object format, {'results': [{'header1': 'value1', 'header2': 'value2'}, {'header1': 'value3', 'header2': 'value4'}, ...]}. Returning results in tabular form does decrease the amount of data being sent across the network but at in certain situations, records can be easier to work with, data-flow currently expects data in the records format. `@ac.authentication_required` ensures that any request sent to this view contains hawk authentication credentials, an example of how to include credentials in your request can be found below.


## Deployment
For examples of deployment to cloud foundry and deployment using Jenkins see the examples of other apps below.


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
