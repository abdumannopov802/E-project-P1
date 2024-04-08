from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.core.mail import send_mail
import logging
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def checkout(request):
    return render(request, 'checkout.html', {})

def contact(request):
    if request.method == 'POST':
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        from_email = request.POST.get("from_email")
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ["akromabdumannopov815@example.com"])
                return render(request, 'contact.html', {'success': True})
            except Exception as error:
                logging.error(error)
                return render(request, 'contact.html', {'error': True})
        else:
            return render(request, 'contact.html', {'error': True})
    else:
        return render(request, 'contact.html', {})

def index(request):
    count = 0
    products = []
    all_products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {'products': all_products, 'categories': categories, 'related_products': all_products})

def product_detail(request, pk):
    product_instace = get_object_or_404(Product, id=pk)
    all_Products = Product.objects.all()
    related_products = []
    for product in all_Products:
        if product.category.id == product_instace.category.id:
            related_products.append(product)
    category_name = product.category.name
    return render(request, 'product-detail.html', {'product': product, 'related_products': related_products, 'category_name': category_name})

def shop_details(request):
    return render(request, 'shop-details.html', {})

def shop_grid(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    sale_products = []
    for product in products:
        if product.sale_off:
            sale_products.append(product)
    return render(request, 'shop-grid.html', {'sale_products': sale_products, 'categories': categories,})

def shopping_cart(request):
    if request.user.is_authenticated:
        # Fetch the current user's cart items
        user_cart_items = Order.objects.filter(customer=request.user.customer, complete=False)
        context = {'cart_items': user_cart_items}
    else:
        context = {'cart_items': None}  # No cart items for non-authenticated users

    return render(request, 'shoping-cart.html', context)


### Authentication <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'authentication/log-in.html')
	
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            for field, errors in signup_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        signup_form = UserCreationForm()
    
    return render(request, 'authentication/sign-up.html', {'signup_form': signup_form})

def user_logout(request):
    logout(request)
    return redirect('home')