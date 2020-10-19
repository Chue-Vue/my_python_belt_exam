from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('add_author', views.add_author),
    path('destroy_author/<int:author_id>', views.destroy_author),
    path('edit_user', views.edit_user),
    path('update_user', views.update_user),
    path('user_quotes/<int:user_id>', views.user_quotes),
    path('like/<int:author_id>/<int:user_id>', views.like)
]