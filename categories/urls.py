from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='categories_index'),
    path('create/', views.create_category, name='create_category'),
]