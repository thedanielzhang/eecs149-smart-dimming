from django.urls import path
from app import views

urlpatterns = [
    path('lights/', views.light_general),
    path('lights/<int:pk>/', views.light_specific),
    path('schedules/', views.schedule_general),
    path('schedules/<int:pk>/', views.schedule_specific),

]
