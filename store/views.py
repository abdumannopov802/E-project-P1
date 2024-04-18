from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from .forms import *
from django.core.mail import send_mail
import logging
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

def checkout(request):
    if request.method == 'GET':
        user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
        total_sum = sum(item.get_total for item in user_cart_items)
        quantity = len(user_cart_items)
        context = [{'item_name': item.product.name, 'item_total': item.product.price * item.quantity} for item in user_cart_items]
        return render(request, 'checkout.html', {'total_sum': total_sum, 'context': context, 'quantity': quantity})
    elif request.method == 'POST':
        user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
        if user_cart_items:
            for item in user_cart_items:
                PurchaseHistory.objects.create(customer=request.user.customer, product=item.product, quantity=item.quantity)
            user_cart_items.delete()
            message_success = "Your order was ACTIVATED successfully!"
            return render(request, 'checkout.html', {'message_success': message_success})
        else:
            message_fail = "Your cart is empty!"
            return render(request, 'checkout.html', {'message_fail': message_fail})
    else:
        return HttpResponseBadRequest("Only GET and POST requests are supported for this endpoint.")


def contact(request):
    count=0
    user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
    total_sum = sum(item.get_total for item in user_cart_items)
    quantity = sum(count+1 for _ in user_cart_items)
    if request.method == 'POST':
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        from_email = request.POST.get("from_email")
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ["akromabdumannopov802@gmail.com"])
                return render(request, 'contact.html', {'success': True, 'total_sum': total_sum, 'quantity': quantity})
            except Exception as error:
                logging.error(error)
                return render(request, 'contact.html', {'error': True, 'total_sum': total_sum, 'quantity': quantity})
        else:
            return render(request, 'contact.html', {'error': True, 'total_sum': total_sum, 'quantity': quantity})
    else:
        return render(request, 'contact.html', {'total_sum': total_sum, 'quantity': quantity})

def index(request):
    if request.user.is_authenticated:
        count = 0
        products = []
        user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
        total_sum = sum(item.get_total for item in user_cart_items)
        quantity = sum(count+1 for _ in user_cart_items)
        all_products = Product.objects.all()
        categories = Category.objects.all()
    else:
        return redirect('login')
    return render(request, 'index.html', {'products': all_products, 'categories': categories, 'related_products': all_products, 'total_sum': total_sum, 'quantity': quantity})

def product_detail(request, pk):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=pk)
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)

        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += quantity
        order_item.save()

        return redirect('product-detail', pk=pk)

    product_instance = get_object_or_404(Product, pk=pk)
    all_products = Product.objects.all()
    related_products = [product for product in all_products if product.category.id == product_instance.category.id]
    category_name = product_instance.category.name

    count=0
    user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
    total_sum = sum(item.get_total for item in user_cart_items)
    quantity = sum(count+1 for _ in user_cart_items)
    return render(request, 'product-detail.html', {'product': product_instance, 'related_products': related_products, 'category_name': category_name, 'total_sum': total_sum, 'quantity': quantity})

def shop_grid(request):
    if request.method == 'GET':
        products = Product.objects.all()
        categories = Category.objects.all()
        count=0
        user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
        total_sum = sum(item.get_total for item in user_cart_items)
        quantity = sum(count+1 for _ in user_cart_items)
        sale_products = []
        for product in products:
            if product.sale_off:
                sale_products.append(product)
    return render(request, 'shop-grid.html', {'sale_products': sale_products, 'categories': categories, 'all_products': products, 'total_sum': total_sum, 'quantity': quantity})

def shop_grid_pk(request, pk):
    if request.method == 'GET':
        search_products = get_list_or_404(Product, category=pk)
        products = Product.objects.all()
        categories = Category.objects.all()
        user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
        total_sum = sum(item.get_total for item in user_cart_items)
        quantity = len(user_cart_items)
    return render(request, 'shop-grid.html', {'categories': categories, 'search_products': search_products, 'all_products': search_products, 'total_sum': total_sum, 'quantity': quantity})

def shopping_cart(request):
    if request.user.is_authenticated:
        count=0
        user_cart_items = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)
        total_sum = sum(item.get_total for item in user_cart_items)
        quantity = sum(count+1 for _ in user_cart_items)
        context = {'cart_items': user_cart_items, 'total_sum': total_sum, 'quantity': quantity}
    else:
        context = {'cart_items': None}
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
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        product = Product.objects.get(pk=product_id)
        # Perform your logic to add the product to the cart
        messages.success(request, 'Product added to cart successfully.')
    return redirect('product-detail', pk=product_id)

def remove_from_cart(request, pk):
    item = get_object_or_404(OrderItem, id=pk)
    item.delete()
    return redirect('shopping-cart')