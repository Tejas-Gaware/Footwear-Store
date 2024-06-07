from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count
import razorpay
from django.views import View
from django.conf import settings
from . forms import *
from django.contrib import messages
from . models import Cart, Category, Contact, Customer, OrderPlaced, Payment, Product, ProductColor
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from Luvin.settings import EMAIL_HOST_USER
import random

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        
    return render(request, 'app/home.html', locals())


@login_required
def contact_us(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST['username']
        email = request.POST['email']
        msg = request.POST['msg']
        
        contact.name = name
        contact.email = email
        contact.message = msg
        contact.save()
        messages.success(request, "Thanks for contacting we will get in touch with you soon!")
        
    return render(request, "app/contact_us.html", locals())


def products(request):
    search = request.GET.get('search') if request.GET.get('search') is not None else ''

    products = Product.objects.filter(
        Q(title__icontains=search) | Q(category__name__icontains=search)
    )
    
    if 'price' in request.GET:
        price = request.GET.get('price')
        products = Product.objects.filter(price__range=(0,price))
    
    if 'gender' in request.GET:
        gender = str(request.GET.get('gender'))
        products = Product.objects.filter(gender=gender)
    
    
    
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories
    }

    return render(request, 'app/products.html', context)

@login_required
def product_view(request,pk):
    try:
        product = Product.objects.get(id=pk)
        print(product)
        return render(request, "/app/product_view.html", context={'product' : product, "totalItem": totalItem})
    except Exception as e:
        print(e)
    
    totalItem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/product_view.html', context={'product': product, "totalItem": totalItem})


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    color = request.GET.get('color-options')
    size = request.GET.get('size-options')
    
    Cart(user=user, product=product, color=color, size=size).save()
    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    
    amount = 0
    for i in cart:
        value = i.quantity * i.product.price
        amount = amount + value
    
    totalAmount = amount + 79.89
    return render(request, 'app/cart.html', locals())


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        
        totalAmount = amount + 79.89
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalAmount':totalAmount,
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        
        totalAmount = amount + 79.89
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalAmount':totalAmount,
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        
        totalAmount = amount + 79.89
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalAmount':totalAmount
        }
        return JsonResponse(data)


class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        
        for p in cart_items:
            value = p.quantity * p.product.price
            amount = amount + value
        
        totalAmount = amount + 79.89
        razorAmount = int(totalAmount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razorAmount, "currency": "INR", "receipt": f'rcpt_${totalAmount}_78${amount}'}
        payment_response = client.order.create(data=data)
        
        order_id = payment_response['id']
        order_status = payment_response['status']
        
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalAmount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        
        return render(request, 'app/checkout.html', locals())


def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    
    user = request.user
    
    customer = Customer.objects.get(id=cust_id)
    
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    paid_price = payment.amount
    payment.save()
    cart = Cart.objects.filter(user=user)
    prod = ""
    for c in cart:
        prod = c.product
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    
    # sending email receipt
    subject = "Order placed successfully!"
    message = f"""Congratulations! your order was placed successfully!\n\nHere's a summary of your order,\nOrder ID\n#{order_id}\n\nPayment ID\n#{payment_id}\n\nCustomer ID\n#lvn2024{cust_id}\n\n{prod}\nAmount paid      ₹{paid_price}/-\n\nThank you for the purchase, we look forward to serving you again soon!\nSincerely,\nLuvin
    """
    email = request.user.email
    recipient_list = [email]
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)
    
    return redirect("orders")


def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    print(request.user.email)
    return render(request, 'app/orders.html', locals())


def qr_generator(request, pk):
    user_id = request.user.id
    i = user_id + random.randint(1000, 11000)
    return render(request, 'app/qr_generator.html', locals())


@login_required
def receipt(request, i, pk):
    order = OrderPlaced.objects.filter(id=pk)
    for od in order:
        user = od.user
        product = od.product.title
        order_id = od.payment.razorpay_order_id
        payment_id = od.payment.razorpay_payment_id
        price = od.payment.amount
        address = od.customer.locality + " " + od.customer.city + "-" + str(od.customer.zipcode) + " " + od.customer.state
        
    return render(request, 'app/receipt.html', locals())


class Profile(View):
    def get(self, request):
        form = CustomerProfileForm()
        address = Customer.objects.filter(user=request.user)
        phone = address[:1]
        return render(request, 'app/profile.html', locals())
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            customer = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            customer.save()
            messages.success(request, "Address saved successfully")
        else:
            messages.warning(request, "Please enter valid information")
        
        address = Customer.objects.filter(user=request.user)
        return redirect('profile')


def delete_address(request, pk):
    address = Customer.objects.filter(id=pk)
    address.delete()
    address = Customer.objects.filter(user=request.user)
    messages.success(request, "Address deleted")
    return redirect('profile')


class updateAddress(View):
    def get(self, request, pk):
        address = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=address)
        return render(request, 'app/updateAddress.html', locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            print(add)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Address updated successfully")
        else:
            messages.warning(request, 'Invalid input')
        
        return redirect('profile')


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/signUp.html', locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account create successfully")
        else:
            messages.warning(request, "Enter valid details")
            
        return render(request, 'app/signUp.html',locals())