from app.api import views

RULES = [
    ('/get-data', views.get_data),
    ('/get-data-authenticated', views.get_data_authenticated),
    ('/train-model', views.train_model),
]
