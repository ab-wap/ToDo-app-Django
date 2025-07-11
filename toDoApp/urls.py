from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('add/', views.add_view, name="add"),
    path('delete/<int:todo_id>/', views.delete_view, name="delete"),
    path('update/<int:todo_id>/', views.update_view, name="update"),
    path('toggle/<int:todo_id>/', views.toggle_view, name="toggle"),
]
