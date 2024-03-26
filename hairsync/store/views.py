"""HairSynC Store Views"""
"""Using csrf_exempt because the website is for ALX demonstration"""
from django.contrib.auth import authenticate, login, logout
from django.db.models import F, ExpressionWrapper, fields, Sum, Q
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from .models import Product, CategoryManager, Category, User, Order, ShoppingCart, CartItem, Address, OrderItem
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError, MultipleObjectsReturned, PermissionDenied, ObjectDoesNotExist
from django.http import QueryDict
from django.core.serializers import serialize
from django.forms.models import model_to_dict


def check_authentication(view_func):
    """
    Decorator to check if a user is authenticated.
    Returns a JSON response with an error message if the user is not authenticated.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


"""Decorator to render the homepage (LANDING PAGE)"""
@require_http_methods(["GET"])
def index(request):
    return render(request, 'store/index.html')


"""REGISTER, LOGIN, AND LOGOUT VIEWS"""
@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = request.POST

        # Use .get() to safely access keys and provide default values
        username = data.get('username', '')
        password = data.get('password', '')
        email = data.get('email', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        # Check if all required fields are provided
        if not all([username, password, email, first_name, last_name]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        user_cart = ShoppingCart(user=user)
        user_cart.save()

        return JsonResponse({"message": "User created successfully"}, status=200)

    except IntegrityError:
        return JsonResponse({"error": "Username or email already exists"}, status=409)

    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"error": "Username and password are required", "code": "invalid_input"}, status=400)

        try:
            email_passed = User.objects.get(email=username)
            username = email_passed.username
        except User.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            return JsonResponse({
                "error": "You are using the same email for Django Admin Dashboard and your newly created user, change one of them.",
                "code": "email_conflict",
                "details": "The email address you provided is associated with multiple user accounts."
            }, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.save()
            return JsonResponse({
                "message": "User logged in successfully",
            })
        else:
            return JsonResponse({
                "error": "Authentication failed. Please verify your username/email and password.",
                "code": "authentication_failed",
                "details": "The provided credentials do not match our records."
            }, status=401)

    except MultiValueDictKeyError as e:
        return JsonResponse({
            "error": f"The form value for attribute {str(e)} is missing",
            "code": "missing_form_value",
            "details": f"The required field {str(e)} was not provided in the request."
        }, status=400)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "success"})

def check_user_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({"user": True})
    return JsonResponse({"user": False})



"""THE START OF PRODUCTS VIEWS AND MANAGEMENT"""
@require_http_methods(["GET"])
def list_all_products(request):
    all_products = Product.objects.all()

    if all_products.exists():
        # Serialize the queryset to JSON format
        products_json = serialize('json', all_products)
        return JsonResponse(products_json, safe=False)
    else:
        return JsonResponse({"error": "No products found, add a product and try again."}, status=404)


@require_http_methods(["GET"])
def fetch_product_by_id(request, id):
    try:
        unique_product = Product.objects.get(product_id=id)
        # Use the custom to_dict method to serialize the product
        product_dict = unique_product.to_dict(request)
        return JsonResponse(product_dict, safe=False)

    except Product.DoesNotExist:
        return JsonResponse({"error": f"Product with ID: {id} was not found."}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def create_new_product(request):
    try:
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity_in_stock = request.POST['quantity_in_stock']
        category = request.POST['category']
        image = request.FILES['image']

    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing"}, status=400)

    try:
        with transaction.atomic():
            # Ensure the category exists before creating the product
            category_obj = Category.objects.get(name=category)
            new_product = Product(name=name, description=description, price=float(price), quantity_in_stock=quantity_in_stock, category=category_obj, image=image)
            new_product.save()
    except (ValueError, ValidationError) as e:
        return JsonResponse({"error": f"{str(e)}"}, status=400)
    except Category.DoesNotExist:
        return JsonResponse({"error": f"Category '{category}' does not exist."}, status=400)

    return JsonResponse({"success": True}, safe=False)


@csrf_exempt
@require_http_methods(["PUT", "POST"])
def update_product_id_details(request, id):
    try:
        product_to_update = Product.objects.get(product_id=id)

        if request.method == 'PUT':
            for field, value in QueryDict(request.body).items():
                if (hasattr(product_to_update, field) and field == "category"):              
                    try:
                        setattr(product_to_update, field, Category.objects.get(name=value))
                    except (ValueError, ValidationError, Category.DoesNotExist) as e:
                        return JsonResponse({"error": f"{str(e)}"}, status=400)
                
                elif (hasattr(product_to_update, field) and field == "image"):
                    return JsonResponse({"error": 'Use POST request to update image'}, status=405)
                
                elif (hasattr(product_to_update, field)):
                    setattr(product_to_update, field, value)
                
                else:
                    return JsonResponse({"error": f"There is no field named {field} in products table."}, status=400)
                
        if request.method == 'POST':
            data = request.POST
            image = request.FILES['image']
            
            for field, value in data.items():
                if (hasattr(product_to_update, field) and field == "category"):                
                    try:
                        setattr(product_to_update, field, Category.objects.get(name=value))
                    except (ValueError, ValidationError, Category.DoesNotExist) as e:
                        return JsonResponse({"error":f"{str(e)}"}, status=400)
                    
                elif (hasattr(product_to_update, 'image')):
                    product_to_update.image = image
                
                elif (hasattr(product_to_update, field)):
                    setattr(product_to_update, field, value)               
                
                else:
                    return JsonResponse({"error": f"There is no field named {field} in products table."}, status=400)

        with transaction.atomic():
            product_to_update.save()
    
    except Product.DoesNotExist as e:
        return JsonResponse({"error": f"Product with ID: {id} was not found."}, status=404)

    return JsonResponse({"success": True}, safe=False)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product_by_id(request, id):
    try:
        product_to_delete = Product.objects.get(product_id=id)
        product_to_delete_details = product_to_delete.to_dict(request)

        product_to_delete.delete()

    except Product.DoesNotExist as e:
        return JsonResponse({"error": f"Product with ID: {id} was not found."}, status=404)
    
    return JsonResponse({"success": True}, safe=False)


"""SEARCH AND FILTERS MANAGEMENT"""
@require_http_methods(["POST", "GET"])
def search_products_and_categories(request):
    try:
        search_term = request.POST['search']

        # Search for products where the name or description matches the search term
        # Include the related Category information in the results
        product_results = Product.objects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term)).select_related('category')

        product_results_json = serialize('json', product_results)

        return JsonResponse(product_results_json, safe=False)
    
    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing."}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def apply_filters_to_search_results(request):
    # Retrieve search results from the session
    search_results = request.session.get('search_results')

    if search_results:
        # Deserialize the search results from the session
        search_results = [Product.objects.get(product_id=product['pk']) for product in search_results]

        # Retrieve filter parameters from the request
        min_price = int(request.POST.get('min_price', 0))
        max_price = int(request.POST.get('max_price', 1_000_000_000))
        category_filter = request.POST.get('category', None)

        # Apply filters to the search results
        filtered_results = [product for product in search_results if min_price <= product.price <= max_price]
        if category_filter:
            filtered_results = [product for product in filtered_results if product.category.name == category_filter]

        # Serialize the filtered search results to JSON format
        filtered_results_json = serialize('json', filtered_results)

        return JsonResponse(filtered_results_json, safe=False)
    else:
        return JsonResponse({"error": "No search results found in session."}, status=404)
    

"""THE START OF CATEGORY VIEW/MANAGEMENT"""
@require_http_methods(["GET"])
def get_list_of_all_product_categories(request):
    list_of_all_categories = Category.objects.all()

    if list_of_all_categories.exists():
        # Serialize the queryset to JSON format
        categories_json = serialize('json', list_of_all_categories)
        return JsonResponse(categories_json, safe=False)
    else:
        return JsonResponse({"error": "No categories found."}, status=404)


@require_http_methods(["GET"])
def get_list_of_all_products_in_category(request, id):
    try:
        category = Category.objects.get(pk=id)
        products_in_category = Product.objects.filter(category=category)

        # Serialize the queryset to JSON format
        products_json = serialize('json', products_in_category)
        return JsonResponse(products_json, safe=False)
    except Category.DoesNotExist:
        return JsonResponse({"error": f"Category with ID: {id} was not found."}, status=404)
    

@require_http_methods(["POST"])
def create_new_product_category(request):
    try:
        name = request.POST["name"]

        new_category = Category(name=name)
        new_category.save()
    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {e} is missing."}, status=400)
    
    return JsonResponse({"success": True}, safe=False)


@require_http_methods(["PUT"])
def update_details_of_category_with_category_id(request, id):
    try:
        category_to_update = Category.objects.get(pk=id)

        name = QueryDict(request.body).get('name')

        if name:
            category_to_update.name = name
            category_to_update.save()
        else:
            return JsonResponse({"error": "The 'name' field is required."}, status=400)

    except Category.DoesNotExist:
        return JsonResponse({"error": f"Category with ID: {id} does not exist."}, status=404)

    return JsonResponse({"success": True}, safe=False)


@require_http_methods(["DELETE"])
def remove_product_category_with_category_id(request, id):
    try:
        category_to_delete = Category.objects.get(pk=id)

        # Assuming to_dict is a method on the Category model that serializes the object
        category_to_delete_details = category_to_delete.to_dict()

        category_to_delete.delete()

    except Category.DoesNotExist:
        return JsonResponse({"error": f"Category with ID: {id} does not exist."}, status=404)
    
    return JsonResponse({"success": True, "deleted_category": category_to_delete_details}, safe=False)



"""USER PROFILE MANAGEMENT"""
@check_authentication
@require_http_methods(["GET"])
def get_user_profile(request):
    try:
        specific_user = User.objects.get(id=request.user.id)
        return JsonResponse({
            'id': specific_user.id,
            'username': specific_user.username,
            'email': specific_user.email,
            'first_name': specific_user.first_name,
            'last_name': specific_user.last_name
        }, safe=False)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist."}, status=404)


@check_authentication
@require_http_methods(["PUT"])
def update_user_profile(request):
    try:
        user_to_update = User.objects.get(id=request.user.id)

        for field, value in QueryDict(request.body).items():
            if (hasattr(user_to_update, field) and field == "password"):                
                try:
                    user_to_update.set_password(value)
                except (ValueError, ValidationError) as e:
                    return JsonResponse({"error": str(e)}, safe=False)
            
            elif (hasattr(user_to_update, field)):
                setattr(user_to_update, field, value)

            else:
                return JsonResponse({"error": f"There is no field named {field} in users table."}, status=404)

        user_to_update.save()      
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist."}, status=404)

    return JsonResponse({"success": True}, safe=False)


@check_authentication
@require_http_methods(["GET"])
def list_orders_placed_by_user(request):
    try:
        orders_placed_by_user = Order.objects.filter(user=request.user)
        
        orders_data = [order.to_dict() for order in orders_placed_by_user]
        return JsonResponse({'orders': orders_data}, safe=False)
    except Order.DoesNotExist:
        return JsonResponse({"error": "No orders found for the user."}, status=404)



"""THE START OF SHOPPING CART MANAGEMENT"""
@check_authentication
@require_http_methods(["GET"])
def get_user_shopping_cart_contents(request):
    try:
        user_id = request.user.id
        cart_contents = ShoppingCart.objects.get(user=user_id)

        cart_items = CartItem.objects.filter(cart=cart_contents)

        # Serialize the cart items to JSON format
        cart_items_json = serialize('json', cart_items)

        return JsonResponse(cart_items_json, safe=False)

    except ShoppingCart.DoesNotExist:
        return JsonResponse({"error": "Shopping cart not found for the user."}, status=404)

    except TypeError:
        return JsonResponse({"error": "An error occurred while retrieving the shopping cart contents."}, status=500)


@check_authentication
@require_http_methods(["POST"])
def add_product_to_cart(request, productId):
    try:
        user_id = request.user.id
        quantity = int(request.POST['quantity'])

        product = Product.objects.get(product_id=productId)
        if quantity > product.quantity_in_stock:
           return JsonResponse({"error": f"Please reduce the quantity to {product.quantity_in_stock} or less, as the current stock is {quantity} items."}, safe=False)


        try:
            # Try to get an existing cart item
            existing_cart_item = CartItem.objects.get(cart=ShoppingCart.objects.get(user=user_id), product=product)
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
            return JsonResponse(existing_cart_item.to_dict(), safe=False)
        except CartItem.DoesNotExist:
            # If no existing cart item, create a new one
            try:
                cart = ShoppingCart.objects.get(user=user_id)
            except ShoppingCart.DoesNotExist:
                # If no shopping cart exists, create one
                cart = ShoppingCart(user=User.objects.get(id=user_id))
                cart.save()
            new_cart_item = CartItem(cart=cart, product=product, quantity=quantity)
            new_cart_item.save()
            return JsonResponse({"success": True}, safe=False)

    except Product.DoesNotExist:
        return JsonResponse({"error": f"Product with ID: {productId} not found."}, status=404)
    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing."}, status=400)


@check_authentication
@require_http_methods(["DELETE"])
def remove_product_from_user_cart(request, productId):
    try:
        user_id = request.user.id
        cart_item_to_delete = CartItem.objects.get(cart=ShoppingCart.objects.get(user=user_id), product=Product.objects.get(product_id=productId))

        cart_item_to_delete_details = cart_item_to_delete.to_dict()

        cart_item_to_delete.delete()

        return JsonResponse({"message": "Item deleted", "item_details": cart_item_to_delete_details}, safe=False)

    except ShoppingCart.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {user_id} does not have an active cart."}, status=404)

    except Product.DoesNotExist:
        return JsonResponse({"error": f"Product with ID: {productId} not found in cart."}, status=404)

    except CartItem.DoesNotExist:
        return JsonResponse({"error": f"CartItem does not exist."}, status=404)


@check_authentication
@require_http_methods(["DELETE", "POST"])
def clear_entire_shopping_cart(request):
    try:
        user_id = request.user.id
        cart_to_clear = ShoppingCart.objects.get(user=user_id)

        cart_to_clear_items = CartItem.objects.filter(cart=cart_to_clear)

        cart_to_clear_items.delete()

        return JsonResponse({"message": "Cart cleared"}, safe=False)

    except ShoppingCart.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {user_id} does not have a cart."}, status=404)
