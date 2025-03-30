from ntpath import join
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail


#from salon.forms import SignUpForm

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

# def cart(request):
#     return render(request, 'cart.html')


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
        # phone_number = request.Post.get('phone_number')

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
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('register')
    
    # Render the registration page template (GET request)
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

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

    return redirect('view_cart')

