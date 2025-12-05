from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:category_id>/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
