from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.home_view, name="home"),
    path('add/', views.add_view, name="add"),
    path('delete/<int:todo_id>/', views.delete_view, name="delete"),
    path('update/<int:todo_id>/', views.update_view, name="update"),
    path('toggle/<int:todo_id>/', views.toggle_view, name="toggle"),
    # path('ajax/tasks/', views.ajax_filtered_tasks, name='ajax_filtered_tasks'),
    # path('ajax/toggle/<int:todo_id>/', views.ajax_toggle_view, name='ajax_toggle'),
]
