from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from allauth.account.views import LoginView


urlpatterns = [
    path('', views.startup, name='startup'),
    path('home/', views.home, name='home'),
    path('be_a_landlord/', views.landlord, name='landlord'),
    path('description/<int:pk>/', views.description, name='description'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('edit/<int:pk>/', views.edit, name='edit'),

    # 👇 custom login view (keep this one only)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='custom_login'),

    # 👇 logout confirmation and execution
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),  # GET shows confirmation
    path('logout/', views.logout_view, name='logout'),  # POST logs out
    path('user_profile/', views.profile, name='profile'),
    path('filter_rooms/', views.filter_rooms, name='filter_rooms'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-municipalities/', views.load_municipalities, name='ajax_load_municipalities'),
]
