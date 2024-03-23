"""HairSynC Store Views"""
from django.contrib.auth import authenticate, login, logout
from django.db.models import F, ExpressionWrapper, fields, Sum
from django.db import IntegrityError
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
from django.core.paginator import Paginator, EmptyPage


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


"""Register, Login, and Logout views"""
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
            user_email_passed_instead = User.objects.get(email=username)
            username = user_email_passed_instead.username
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