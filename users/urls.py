from django.urls import path, include
from . import views

urlpatterns = [    
    path("generate_keys/", views.generate_keys, name="generate_keys"),
    path("show_my_keys/", views.show_my_keys, name="show_my_keys"),
]
