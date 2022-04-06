from __future__ import unicode_literals, absolute_import
from . import views
from django.urls import path
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #Login paths
    path('', views.new_login),
    path('signup/', views.newsignup),

    #Main paths
    path('resources/', views.resources, name='resources'),
    path('talks/', views.talks, name='talks'),
    path('connection/', views.connection, name='connection'),
    path('scholarship/', views.scholarship, name="scholarship"),
    path('main', views.new_login, name='main'),

    #Admin paths
    path('admin', views.admin, name='admin'), 
    path('delete/', views.delete, name='delete'),
    path('analysis', views.popular_resources, name="analysis"),

    #Connection paths
    path('search', views.search, name="search"),
    path("addfriend/<str:name1>/<str:name2>", views.addFriend, name="addFriend"),
    path("getother/<str:name>", views.get_other, name="getoher"),
    path("chat/<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),

    #Other
    path('logout/', views.logout_web, name="logout"),
    path('personal/', views.personal, name="personal")
]
