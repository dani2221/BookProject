from django.shortcuts import render, redirect
from .models import Book, Order, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CheckoutForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


# Create your views here.
def index(request):
    if request.method == 'POST':
        try:
            search = request.POST['search']
            qs = Book.objects.filter(quantity__gt=0, title__contains=search)
            return render(request, "index.html", {"books": qs})
        except:
            print(request.user.is_authenticated)
            if not request.user.is_authenticated:
                return redirect('login')
            book = request.POST['book']
            cart = Cart.objects.filter(user=request.user, active=True).first()
            if cart is None:
                cart = Cart(user=request.user, active=True)
                cart.save()
            book_item = Book.objects.get(title=book)
            cart_item = CartItem.objects.filter(cart=cart, book=book_item).first()
            if cart_item is None:
                cart_item = CartItem(cart=cart, book=book_item, quantity=1)
                cart_item.save()
            else:
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()

    qs = Book.objects.filter(quantity__gt=0)
    if request.user.is_authenticated:
        cart_items = list(CartItem.objects.filter(cart__user=request.user, cart__active=True))
        cart_items_sum = 0
        for item in cart_items:
            cart_items_sum += item.quantity
        print(cart_items)
    else:
        cart_items_sum = 'Најави се'
    return render(request, "index.html", {"books": qs, "cart_items": cart_items_sum})


def detail_view(request, title):
    is_added = False
    if request.method == 'POST':
        try:
            search = request.POST['search']
            qs = Book.objects.filter(quantity__gt=0, title__contains=search)
            return render(request, "index.html", {"books": qs})
        except:
            print(request.user.is_authenticated)
            if not request.user.is_authenticated:
                return redirect('login')
            book = request.POST['book']
            cart = Cart.objects.filter(user=request.user, active=True).first()
            if cart is None:
                cart = Cart(user=request.user, active=True)
                cart.save()
            book_item = Book.objects.get(title=book)
            cart_item = CartItem.objects.filter(cart=cart, book=book_item).first()
            if cart_item is None:
                cart_item = CartItem(cart=cart, book=book_item, quantity=1)
                cart_item.save()
            else:
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
            is_added = True

    qs = Book.objects.filter(title=title).get()

    if request.user.is_authenticated:
        cart_items = list(CartItem.objects.filter(cart__user=request.user, cart__active=True))
        cart_items_sum = 0
        for item in cart_items:
            cart_items_sum += item.quantity
    else:
        cart_items_sum = 'Најави се'
    return render(request, "book.html", {"book": qs, "cart_items": cart_items_sum, "added_new": is_added})


def cart(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    cart_items = CartItem.objects.filter(cart__user=request.user, cart__active=True)
    total = 0
    for item in list(cart_items):
        total += item.quantity * item.book.price
    for item in cart_items:
        item.total_price = item.quantity * item.book.price
    print(cart_items)
    return render(request, "cart.html", {"items": cart_items, "total_amount": total})


def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.filter(active=True, user=request.user).first()
            cart.active = False
            cart.save()
            order = Order(cart=cart, full_name=request.POST.get('full_name'), address=request.POST.get('address'), delivery_status='new')
            order.save()
            print(order)
            return redirect('/orders')
    else:
        form = CheckoutForm()

    context = {
        'form': form
    }
    return render(request, 'payment.html', context)


def order_list_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    orders = Order.objects.filter(cart__user=request.user).order_by('-id')

    for order in orders:
        order.cart_items = CartItem.objects.filter(cart=order.cart)
        total = 0
        for item in list(order.cart_items):
            total += item.quantity * item.book.price
        order.total = total

    context = {
        'orders': orders
    }

    return render(request, 'orders.html', context)

