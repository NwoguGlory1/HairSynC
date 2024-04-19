from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "store"
urlpatterns = [
    # Home Page
    path('', views.index, name='index'), # Home page

    path('about_us/', views.about_us, name='about_us'),

    # Register, login, and logout
    path('register/', views.register, name='register'), # User registration
    path('register_form/', views.register_form, name='register_form'),
    path('login/', views.login_view, name='login'), # User login
    path('login_page/', views.login_page, name='login_page'),
    path('logout/', views.logout_view, name='logout'), # User logout
    path('user_status/', views.check_user_authentication, name='user_status'), # Check User Authentication
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

    # Products Management
    path('products/', views.list_all_products, name='products'),
    path('products/<int:id>/', views.fetch_product_by_id, name='get-product-details'),
    path('products/create/', views.create_new_product, name='create-new-product'),
    path('products/<int:id>/update/', views.update_product_id_details, name='update-product-details'),
    path('products/<int:id>/delete/', views.delete_product_by_id, name='delete-product'),
    path('bonestraight/', views.bonestraight, name='bonestraight'),
    path('blondwavyhair/', views.blondwavyhair, name='blondwavyhair'),
    path('watercurls/', views.watercurls, name='watercurls'),
    path('orsconditioner/', views.orsconditioner, name='orsconditioner'),
    path('wavyhair/', views.wavyhair, name='wavyhair'),
    path('hawaiiansilky/', views.hawaiiansilky, name='hawaiiansilky'),
    path('doubledrawn/', views.doubledrawn, name='doubledrawn'),
    path('pixiecurls/', views.pixiecurl, name='pixiecurls'),


    # Search and Filters
    path('search/', views.search_products_and_categories, name='search-products-and-categories'),
    path('filters/', views.apply_filters_to_search_results, name='apply-filters'),


    # Categories
    path('categories/', views.get_list_of_all_product_categories, name='list-all-categories'),
    path('categories/<int:id>/', views.get_list_of_all_products_in_category, name='list-all-products-in-category'),
    path('categories/create/', views.create_new_product_category, name='create-new-category'),
    path('categories/<int:id>/update/', views.update_details_of_category_with_category_id, name='update-category-details'),
    path('categories/<int:id>/delete/', views.remove_product_category_with_category_id, name='delete-category'),
    path('categories/<str:category_name>/', views.get_category_by_name, name='get_category_by_name'),
    path('straight/', views.straight_category, name='straight'),
    path('hair_products/', views.hair_products_category, name='hair_products'),
    path('coily/', views.coily_category, name='coily'),
    path('wavy/', views.wavy_category, name='wavy'),

    # USER
    path('userprofile/', views.get_user_profile, name='userprofile'),
    path('users/update/', views.update_user_profile, name='update-user-profile'),
    path('users/orders/', views.list_orders_placed_by_user, name='list-user-orders'),
    #path('userprofile/', views.userprofile, name='userprofile'),
    
    
    # Shopping Cart
    path('users/cart/', views.get_user_shopping_cart_contents, name='cart'),
    path('users/cart/add/<int:productId>/', views.add_product_to_cart, name='add-product-to-cart'),
    path('users/cart/remove/<int:productId>/', views.remove_product_from_user_cart, name='remove-product-from-cart'),
    path('users/cart/clear/', views.clear_entire_shopping_cart, name='clear-cart'),
    path('users/cart/item-count/', views.get_cart_item_count, name='get_cart_item_count'),


    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('process_checkout/', views.process_checkout, name='process_checkout'),
    path('success/', views.success, name='success'),


    # Order Management
    path('orders/', views.get_list_of_all_orders, name='list-all-orders'),
    path('orders/<int:id>/', views.get_details_of_order_with_order_id, name='get-order-details'),
    path('users/orders/create/', views.create_new_order, name='create-new-order'),
    path('orders/<int:id>/cancel/', views.cancel_order_with_order_id, name='cancel-order'),


    # Shipping and Address
    path('shipping-options/', views.get_available_shipping_options, name='get-shipping-options'),
    path('users/addresses/', views.get_user_saved_addresses, name='get-user-addresses'),
    #path('users/addresses/create/', views.add_address, name='add-address'),
    path('add_address', views.add_address, name='add_address'),
    path('users/addresses/<int:id>/update/', views.update_details_of_address_with_address_id, name='update-address-details'),
    path('users/addresses/<int:id>/delete/', views.delete_address_with_address_id, name='delete-address'),
    path('shipping-options/', views.get_shipping_options, name='get_shipping_options'),

]


