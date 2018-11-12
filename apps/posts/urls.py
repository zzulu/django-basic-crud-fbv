from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('new/', views.post_create, name='create'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('<int:pk>/edit/', views.post_update, name='update'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),
    path('<int:post_id>/comments/new', views.comment_create, name='comments_create'),
    path('<int:post_id>/comments/<int:pk>/delete', views.comment_delete, name='comments_delete'),
]
