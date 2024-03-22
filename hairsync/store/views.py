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
from django.core.exceptions import ValidationError, MultipleObjectsReturned, PermissionDenied
from django.http import QueryDict
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage

