
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem 

def get_customer(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "email": f"{request.user.username}@test.com"
        }
    )
    return customer
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('view_cart')
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity

        items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })

        total += item_total

    return render(request, 'shop/cart.html', {'items': items, 'total': total})
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart

    return redirect('view_cart')
def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)   

        user = authenticate(request, username=username, password=password)

        print("USER:", user)        

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'shop/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')

        user = User.objects.create_user(username=username, password=password)

        Customer.objects.create(
            user=user,
            name=username,
            email=f"{username}@test.com"
        )

        login(request, user)
        return redirect('/')

@login_required
def checkout(request):
    if request.method != "POST":
        return redirect('view_cart')

    customer = get_customer(request)
    cart = Cart.objects.filter(customer=customer).first()

    if not cart or not cart.cartitem_set.exists():
        return redirect('view_cart')

    order = Order.objects.create(customer=customer)

    for item in cart.cartitem_set.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart.cartitem_set.all().delete()

    return render(request, 'shop/order_success.html', {'order': order})
    
def user_logout(request):
    logout(request)
    return redirect('/')
