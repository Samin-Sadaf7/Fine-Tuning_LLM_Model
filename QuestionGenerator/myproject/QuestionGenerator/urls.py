from django.urls import path

from . import views

urlpatterns = [
    path('response/', views.response, name='response'),
    path('echo/<str:param>/', views.echo_view, name='echo'),  
]
