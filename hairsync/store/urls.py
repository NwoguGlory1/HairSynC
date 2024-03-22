from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    # Home Page
    path('', views.index, name='index'), # Home page

    # Authentication
    path('register/', views.register, name='register'), # User registration
    path('login/', views.login_view, name='login'), # User login
    path('logout/', views.logout_view, name='logout'), # User logout
    path('user_status/', views.show_logged_in_user_id, name='user_status'), # Show logged-in user ID
]