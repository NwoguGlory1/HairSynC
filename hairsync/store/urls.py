from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    # Home Page
    path('', views.index, name='index'), # Home page

    # Register, login, and logout
    path('register/', views.register, name='register'), # User registration
    path('login/', views.login_view, name='login'), # User login
    path('logout/', views.logout_view, name='logout'), # User logout
    path('user_status/', views.check_user_authentication, name='user_status'), # Check User Authentication


    # Product Management
    path('products/', views.list_all_products, name='list-all-products'),
    path('products/<int:id>/', views.fetch_product_by_id, name='get-product-details'),
    path('products/create/', views.create_new_product, name='create-new-product'),
    path('products/<int:id>/update/', views.update_product_id_details, name='update-product-details'),
    path('products/<int:id>/delete/', views.delete_product_by_id, name='delete-product'),
    
    ]


