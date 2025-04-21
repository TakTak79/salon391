from datetime import date, datetime
import json
from ntpath import join
import random
from typing import Self
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from django.core.mail import send_mail
from django_registration.backends import *
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email=email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send()

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk)+str(timestamp)+str(user.is_active)
    
generate_token = TokenGenerator()

# Create your views here.
def index(request):
    all_services = Service.objects.all()
    return render(request,'index.html', {'services':all_services})

def about(request):
    return render(request, 'about.html')
    
def booking(request):
    all_services = Service.objects.all()
    return render(request, 'book.html', {'services':all_services})

def services(request):
    all_services = Service.objects.all()
    return render(request, 'services.html', {'services':all_services})

def shop(request):
    all_products = Product.objects.all()
    return render(request, 'shop.html', {'products':all_products})


def activate_user(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user=None
    if user and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Email is verified, you can now login')
        return redirect(reverse('login_page'))
    return render(request, 'authentication/activate-failed.html',{'user':user})

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('activate.html',{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    send_mail(email_subject,email_body, "browsalon3@gmail.com", [str(user.email)])
    



def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('login_page')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('login_page')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('index')
    
    # Render the login page template (GET request)
    return render(request, 'login.html')

# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('register')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=username
        )
        
        # Set the user's password and save the user object
        user.is_active=False
        user.set_password(password)
        user.save()
        send_activation_email(user,request)
        
        # Display an information message indicating successful account creation
        messages.info(request, "We sent you an email to verify your account")
        return redirect('login_page')
    
    # Render the registration page template (GET request)
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def view_cart(request):
    all_products = Product.objects.all()
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.cost * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price,'products':all_products })

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity <= 1:
        cart_item.delete()
    else:
        cart_item.quantity= cart_item.quantity -1
        cart_item.save()
    return redirect('view_cart')

def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.cost * item.quantity for item in cart_items)
    user = request.user
    user_email = user.email
    date = datetime.today()
    items=[]
    for item in cart_items:
        items.append(item.product.name +": " + str(item.quantity))
        item.delete()

    #Email to user
    send_mail(
    "Order Recieved",
    "Your order has been sent to the owner. When the order is approved you will recieve an email. \n"+'\n'.join(items) + "Total Price is: "+ str(total_price) +"\nThank you for ordering from Brow Salon LLC.",
    "browsalon3@gmail.com",
    [str(user.email)],
    fail_silently=False,
    )

    #Email to owner
    send_mail(
    "Order Recieved",
    "Order from: " + str(user_email)+"\n" + '\n'.join(items) + "\nTotal price is: " + str(total_price),
    "browsalon3@gmail.com",
    ["browsalon3@gmail.com"],
    fail_silently=False,
    )

    #Save order to database
    order = Order()
    order.itemList = json.dumps(items)
    order.user = user
    #order.date_added = date

    order.order_number = str(request.user.id) +str(random.randrange(100,300)) +  '-' + date.strftime('%m-%d-%Y')
    order.save()

    return redirect('view_cart')

def view_profile(request):
    all_orders=Order.objects.filter(user=request.user)
    jsonDec = json.decoder.JSONDecoder()
    # order_numbers=[]
    # order_dates=[]
    # order_contents=[]
    orders=[]
    for order in all_orders:
       orders.append([order.order_number,order.date_added, jsonDec.decode(order.itemList)])

    return render(request, 'profile.html', {'orders': orders })

def reset_passowrd(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user is None:
            # Display an information message if the user acoount does not exsist 
            messages.info(request, "No account with this email adress")
            return redirect('reset_password')

        if user.exists():
            current_site = get_current_site(request)
            email_subject = 'Reset your Password'
            email_body = render_to_string('reset_email.html',{
                'domain':current_site,
                'email': email
            })
            send_mail(
                email_subject,
                email_body, 
                'browsalon3@gmail.com',
                [str(email)],
                fail_silently=False,
                )
            messages.info(request, "Email has been sent to "+ email)
    return render(request, 'reset_password.html')


def new_password(request, email):
    if request.method == 'POST':

        password = request.POST.get('password')

        if request.user.is_authenticated:
            user = request.user
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            user = User.objects.filter(email=email)
            user[0].set_password(password)
            user[0].save()
            login(request, user[0])
            return redirect('index')
    return render(request, 'new_password.html')