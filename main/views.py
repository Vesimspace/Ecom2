from django.shortcuts import render, redirect
from .models import Banner, Category, Brand, Product, ProductAttribute, Order, OrderItems, ProductReview, Wishlist, Address
from django.db.models import Max, Min, Count, Avg
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.template.loader import render_to_string
from . forms import RegisterForm, ReviewForm, AddressForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

def home(request):
    banners = Banner.objects.all().order_by('-id')
    data = Product.objects.filter(featured = True).order_by('-id')
    return render(request, 'index.html', {'data': data, 'banners': banners})

def categories(request):
    data = Category.objects.all().order_by('-id')
    return render(request, 'categories.html', {'data': data})

def brands(request):
    data = Brand.objects.all().order_by('-id')
    return render(request, 'brands.html', {'data': data})

def products(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:3]
    min_price = ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))
    return render(request, 'products.html', {
        'data': data,
        'total_data': total_data,
        'min_price': min_price,
        'max_price': max_price,
        })

def product_list(request, category_id):
    category = Category.objects.get(id=category_id)
    data = Product.objects.filter(category=category ).order_by('-id')


    return render(request, 'product_list.html', {'data': data})


def brand_product_list(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand ).order_by('-id')

    return render(request, 'product_list.html', {'data': data, 'brands': brands})

def product_page(request, slug , id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values('color__id', 'color__title', 'color__color_code').distinct()
    sizes = ProductAttribute.objects.filter(product=product).values('size__id', 'size__title', 'price', 'color__id').distinct()
    reviewForm = ReviewForm()

    canAdd = True
    reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd=False

    reviews = ProductReview.objects.filter(product=product)

    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))

    return render(request, 'product_page.html', {'product': product, 'related_products': related_products, 'colors': colors, 'sizes': sizes, 'reviewForm': reviewForm, 'canAdd':canAdd, 'reviews':reviews, 'avg_reviews':avg_reviews})


def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q)
    return render(request, 'search.html', {'data': data})

def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    all_products = Product.objects.all().order_by('-id').distinct()
    all_products = all_products.filter(productattribute__price__gte = minPrice)
    all_products = all_products.filter(productattribute__price__lte = maxPrice)
    if len(colors) > 0:
        all_products = all_products.filter(productattribute__color__id__in = colors).distinct()
    if len(categories) > 0:
        all_products = all_products.filter(category__id__in = categories).distinct()
    if len(brands) > 0:
        all_products = all_products.filter(brand__id__in = brands).distinct()
    if len(sizes) > 0:
        all_products = all_products.filter(productattribute__size__id__in = sizes).distinct()
    template = render_to_string('ajax/products.html', {'data': all_products})

    return JsonResponse({'data':template})

def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    template = render_to_string('ajax/products.html', {'data': data})
    return JsonResponse({'data':template})

def add_to_cart(request):
    # del request.session['cartdata']
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'image':request.GET['image'],
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
    }

# Update cart data after click
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_product)
            request.session['cartdata'] = cart_data 
    else:
        request.session['cartdata'] = cart_product
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})

def cart(request):
    total_amount = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amount += int(item['qty'])*float(item['price'])
        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amount': total_amount})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amount':total_amount})


def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty'])*float(item['price'])
    template = render_to_string('ajax/cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amount': total_amount})
    return JsonResponse({'data':template, 'totalitems': len(request.session['cartdata'])})
        
def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty'])*float(item['price'])
    template = render_to_string('ajax/cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amount': total_amount})
    return JsonResponse({'data':template, 'totalitems': len(request.session['cartdata'])})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    form = RegisterForm
    return render(request, 'registration/register.html', {'form': form})

@login_required
def checkout(request):
    total_amount = 0
    totalAmount = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmount += int(item['qty'])*float(item['price'])

        order = Order.objects.create(
            user = request.user,
            total_amount = totalAmount,
        )
        for p_id, item in request.session['cartdata'].items():
            totalAmount += int(item['qty'])*float(item['price'])

            items = OrderItems.objects.create(
                order = order,
                invoice_number = 'INV-'+str(order.id),
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty'])*float(item['price']),
            )
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amount,
            'item_name': 'OrderNo-'+str(order.id),
            'invoice': 'INV-'+str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        address = Address.objects.filter(user=request.user, status=True).first()
        return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amount': total_amount, 'form': form, 'address': address})

@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})

@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')

def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		rating=request.POST['rating'],
		)
    data={
        'user':user.username,
        'review_text':request.POST['review_text'],
        'rating':request.POST['rating'],
    }

    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))


    return JsonResponse({'bool':True, 'data':data, 'avg_reviews':avg_reviews})

import calendar
def my_dashboard(request):
    orders = Order.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['month'])
    return render(request, 'user/dashboard.html', {'monthNumber':monthNumber, 'totalOrders':totalOrders})

def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html', {'orders': orders})


def my_order_items(request, id):
    order = Order.objects.get(pk=id)
    orderitems = OrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html', {'orderitems': orderitems})

def wishlist(request):
	pid=request.GET["product"]
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)

def my_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html', {'wishlist': wishlist})

def reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html', {'reviews': reviews})

def address(request):
    address = Address.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/address.html', {'address': address})

def save_address(request):
    message = None
    if request.method== 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                    Address.objects.update(status=False)
            saveForm.save()
            message = 'Data has been saved...'
    form = AddressForm
    return render(request, 'user/save-address.html', {'form': form, 'message': message})


def activate_address(request):
    a_id = str(request.GET['id'])
    Address.objects.update(status=False)
    Address.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool': True})

def profile(request):
    message = None
    if request.method== 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            message = 'Data has been saved...'

    form = ProfileForm(instance=request.user)
    return render(request, 'user/profile.html', {'form': form, 'message': message})

def update_address(request, id):
    address = Address.objects.get(pk=id)
    message = None
    if request.method== 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                    Address.objects.update(status=False)
            saveForm.save()
            message = 'Data has been saved...'
    form = AddressForm(instance=address)
    return render(request, 'user/update-address.html', {'form': form, 'message': message})
