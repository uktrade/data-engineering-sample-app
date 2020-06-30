# Data Engineering Sample App
A minimal example of how to use the [data-engineering-common](https://github.com/uktrade/data-engineering-common/) repository to create a lightweight Flask, hawk authenticated app.

## Installation
This installation is set up for installing on `localhost`, for a Docker workflow see the examples of other apps based on `data-engineering-common` below.

1. Clone repository
2. Create a python virtual environment, e.g. if using [virtualenv](https://virtualenv.pypa.io/en/stable/index.html) `virtualenv venv`
3. Activate the virtualenv, e.g. `source venv/bin/activate`
4. Install python libraries, `pip install -r requirements.txt`
5. Configure the app database connection, edit the `database_url` parameter in the `app/config/defaults.yml` file if neccessary
6. Configure the app cache connection, edit the `cache` parameters in the `app/config/defaults.yml` file if neccessary
7. Install postgres and redis if not already installed
8. Create app database and tables, `python manage.py dev db --create`
9. Create a hawk user: `python manage.py dev add_hawk_user --client_id client_id1 --client_key client_key1 --client_scope '*' --description user1`
10. Run the application server, `flask run`
11. Test the application server, 
    * `python scripts/get_data.py`
    * `python scripts/get_data_authenticated.py`

Note: The `requirements.txt` file includes a reference to the `data-engineering-common` repo, if a newer version of the repo is released you may need to manually uninstall the old version before reinstalling the newer version. `pip remove data-engineering-common`.

## Files
`app/`: basically where all the app logic lives
`app/api`: api logic, routes and views essentially
`app/api/routes.py`: The list of urls that make up the api and their corresponding views. There are 3 routes here,
* `/get-data`: an unauthenticated route
* `/get-data-authenticated`: a hawk authenticated route
* `/train-model`: a route to trigger some process on the app server
* additional routes are also inherited from the `data-engineering-common` repo, e.g. `/healthcheck` which is used by Cloud Foundry to periodically check whether the app server is running without any issues

`app/api/views.py`: Here lies the python implementations of the api routes. `get_data` is a fairly simple view. `get_data_authenticated` showcases how to write a hawk authenticated view, it does this by using several decorators, 

* `json_error` is for making any errors more meaningful
* `response_orientation_decorator` is used for managing the data structure of the returned data, there are two options, `tabular` and `records` (inspired by pandas dataframes and their `to_dict` method). `tabular` will return the data in the form, `{'headers': ['header1', 'header2'], 'values': [('value1', 'value2'), ('value3', 'value4'), ...]}`, `records` will return data in json object format, `{'results': [{'header1': 'value1', 'header2': 'value2'}, {'header1': 'value3', 'header2': 'value4'}, ...]}`. Returning results in tabular form does decrease the amount of data being sent across the network but at in certain situations, records can be easier to work with, data-flow currently expects data in the records format. 
* `@ac.authentication_required` ensures that any request sent to this view contains hawk authentication credentials, an example of how to include credentials in your request can be found below.
* `@ac.authorization_required` ensures that the authenciated user has the correct permissions to access the route, this is managed by the user's scope which is set when creating a Hawk user, in most cases an authenticated user will have permission to use all api routes.

When returning a response object it is important to use the `flask_app.make_response` method because it sets various headers in the response which are used for Hawk response authentication.

`app/application`: Most of the app creation and configuration is managed by `data-engineering-common` app and environment variables which can be set in `app/config/defaults.yml` and `.env`, but some config still lives in here, e.g. where to find the `app/config/defaults.yml` file.

`app/commands`: Here lives some command line commands for mostly development and adminstrative tasks for the app.
`app/commands/__init__.py`: The list of commands/command groups to register to the flask app can be found here, the registration actually occurs in the `data-engineering-common` code.
`app/commands/dev.py`: There are a few important command groups in here, 
* `db`: database manipulation, creating, recreating and dropping databases. In most cases you should only need to use the create command during installation, but if you are doing more complex things like adding and updating models you might use some of the other commands in this command group. For more info at the command line type, `python manage.py dev db --help`.
* `add_hawk_user`: This command requires several arguments, 
  * `client_id` : this is the id you assign to someone who is requesting something from your app 
  * `client_key`: this is the id you assign to someone who is requesting something from your app
  * `client_scope` : Not 100% sure but this should be a list of routes the user can access, but in most cases you can just set this to `'*'`
  * `description`

`app/config/defaults.yml`: A list of the config arguments and their default values
* `app` arguments are general config needed for the app
* `cache` arguments in general configure how the redis database is configured, the redis database is used for Hawk authentication
* `access_control`: hawk configuration

`manage.py` a convenience script for running flask commands, mostly it helps set up the environment when running commands

`README.md`

`requirements.txt`: a list of python packages required to run the app, `data-engineering-common` dependency can be found in here

`scripts`: some scripts to demonstrate how a hawk authenticated request is constructed and how other applications make requests to this application

`scripts/get_data_authenticated`: An example of a hawk authenticated request using the `requests` and `mohawk` python libraries. After installing the app and running it with `flask run` try running this script.

`scripts/get_data`: An example of a non hawk authenticated request.

`scripts/train_model`: A simple example of how to make to a call to an api endpoint to trigger some action. Whilst on this topic, if your process takes a long time to run, as is the case with most model training, you may run into issues with request timeouts. A solution to this may be to use a task queue solution like `celery` or to instead schedule this task to run with something like Jenkins, there are examples of this in other data-engineering apps. In the case of a task queue, the app making the request, e.g. data-flow may also wish to poll your app to check the status of the training of the model, for this you would need either a additonal view which can check the state of the task or modify the existing view so that if a task id is provided as an argument it will check the status of corresponding to that task id instead of creating a new task.

## Deployment
For examples of deployment to cloud foundry and deployment using Jenkins see the examples of other apps below.

## Code formatting 
Other data-engineering apps use Black and flake8 for code formatting, you can look there for inspiration.

## Other Data Engineering Apps
* https://github.com/uktrade/data-engineering-common
* https://github.com/uktrade/countries-of-interest-service
* https://github.com/uktrade/data-store-service
* https://github.com/uktrade/data-store-uploader

## Additional resources
https://www.cloud.service.gov.uk/ go through some of these examples to learn about how to deploy on Cloud Foundry
