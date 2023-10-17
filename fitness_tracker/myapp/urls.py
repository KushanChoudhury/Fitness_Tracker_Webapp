from django.contrib import admin
from django.urls import path,include
from myapp import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("",views.index,name='home'),
    path("contact",views.contact,name='contact'),
    path("login",views.login_view,name='login'),
    path("signup",views.signup,name='signup'),
    path("dashboard",views.dashboard,name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('exercise/', views.exercise_view, name='exercise'),
    path('mark_completed/<str:module_id>/', views.mark_as_completed, name='mark_as_completed'),
    path('update', views.update_view, name='update'),
]
