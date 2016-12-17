from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import F, Sum
from .models import Product, Genre, Artist, Admin, Order, Billing, Shipping, Product_orders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import stripe
###################################### USER ####################################################
def home(request):

    return render(request, "dope_vinyl/home.html")

def front_allproducts(request):
    cart = request.session.get('cart', {})
    length = sum(cart.values())
    try:
        sort=request.POST['sort']
    except:
        sort = 'title'
    if request.method=='GET':
        try:
            products = Product.objects.filter(title__contains=request.GET['search_title']) | Product.objects.filter(artist__name__contains=request.GET['search_title']) |Product.objects.filter(price__contains=request.GET['search_title'])
        except:
            products = Product.objects.all().order_by(sort)
    else:
        products = Product.objects.all().order_by(sort)

    paginator = Paginator(products,15)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    genres = Genre.objects.all()
    context = {
        'products' : products,
        'genres' : genres,
        'sort_current' : sort,
        'length': length,
    }
    return render(request, "dope_vinyl/front_allproducts.html", context)

def front_allproducts_cat(request, id):
    cart = request.session.get('cart', {})
    length = sum(cart.values())
    try:
        sort=request.POST['sort']
    except:
        sort = 'title'
    if request.method=='GET':
        try:
            products = Product.objects.filter(genre=id).filter(title__contains=request.GET['search_title'])
        except:
            products = Product.objects.filter(genre=id).order_by(sort)
    else:
        products = Product.objects.filter(genre=id).order_by(sort)
    paginator = Paginator(products,15)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    genres = Genre.objects.filter(id=id)
    context = {
        'products' : products,
        'sort_current' : sort,
        'genres' : genres,
        'length' : length
    }
    return render(request, "dope_vinyl/front_allproducts.html", context)

def front_productpage(request, id):
    cart = request.session.get('cart', {})
    length = sum(cart.values())

    product = Product.objects.get(id=id)
    similar_products = Product.objects.filter(genre=product.genre).exclude(id=product.id)

    context = {
        'product': product,
        'similar_products': similar_products,
        'length': length,
        }
    return render(request, "dope_vinyl/front_productpage.html", context)

def buy(request, id):
    cart = request.session.get('cart', {})

    product = Product.objects.get(id=id)
    product_id = str(product.id)

    if product_id not in cart:
        cart[product_id] = 1
        messages.success(request, "Item added to the cart")

    else:
        cart[product_id] += 1
        messages.success(request, "Again? You must really like this dope vinyl.")
    request.session['cart'] = cart

    return redirect('product_page', id=product.id)

def carts(request):
    cart = request.session.get('cart', {})
    length = sum(cart.values())

    cart_list = []
    sum_total = 0

    for product_id, quantity in cart.items():
            the_product = Product.objects.get(id=int(product_id))
            the_price = quantity * the_product.price
            cart_list.append([the_product, quantity, the_price])
            sum_total += the_price

    context = {
        'length': length,
        'cart_list': cart_list,
        'total': sum_total,
    }
    return render(request, "dope_vinyl/front_shoppingcart.html", context)

def deletecart_item(request, key_id):
    cart = request.session.get('cart', {})
    new_cart = {}
    for key,value in cart.items():
        if key != key_id:
            new_cart[key] = value

    request.session['cart'] = new_cart

    return redirect('/carts')

def billing_shipping(request):

    if request.method == "POST":
        stripe.api_key = "sk_test_MtYKfrdjHXRPAAuSul1W5m5B"
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=1000,
                currency="USD",
                source=token,
                description="Example charge"
            )
            cart = request.session.get('cart', {})
            cart_list = []
            sum_total = 0
            for product_id, quantity in cart.items():
                the_product = Product.objects.get(id=int(product_id))
                the_price = quantity * the_product.price
                cart_list.append([the_product, quantity, the_price])
                sum_total += the_price

            shipping = Shipping.objects.create(ship_first_name=request.POST['ship_first_name'], ship_last_name=request.POST['ship_last_name'], ship_address1=request.POST['ship_address1'], ship_address2=request.POST['ship_address2'], ship_city=request.POST['ship_city'], ship_state=request.POST['ship_state'], ship_zip=request.POST['ship_zip'])

            billing = Billing.objects.create(bill_first_name=request.POST['bill_first_name'], bill_last_name=request.POST['bill_last_name'], bill_address1=request.POST['bill_address1'], bill_address2=request.POST['bill_address2'], bill_city=request.POST['bill_city'], bill_state=request.POST['bill_state'], bill_zip=request.POST['bill_zip'])

            order = Order.objects.create(shipping=shipping, billing=billing, total=sum_total, status="Order In Process")

            for product,quantity,total_price in cart_list:
                Product_orders.objects.create(orders=order, products=product, quantity=quantity)

            test = Product_orders.objects.filter(orders=3)
            print test
            print "SUCCESSFULLLLLLLLLLLLLLLLL"
            #purchased
            return redirect('/checkout')

        except stripe.error.CardError as e:
         # The card has been declined
            pass

            return redirect('/carts')

def checkout(request):
    if "cart" in request.session:
        request.session.pop("cart")
    return redirect('/front_allproducts')
       # return redirect('/carts')
       #after testing route back to all products page
###################################### ADMIN ###################################################
def admin(request):
    return render(request, "dope_vinyl/adminlogin.html")

def adminlogin(request):
    if request.method == "POST":
        admin = Admin.objects.login(request.POST)

        if not admin:
            messages.error(request, "Invalid login credentials!")
        else:
            request.session['logged_admin'] = admin.id
            return redirect('/dashboard/orders')
    return redirect('/admin')

### justin's is: justin.sucks@gmail.com password: dope. Because he sucks.
### we put one admin into the DB's Admin table.
###     The login is: dope.vinyl.admin@gmail.com (all lowercase)
###     The password is: dope (all lowercase)
def adminlogout(request):
    if 'logged_admin' in request.session:
        request.session.pop('logged_admin')
    return redirect('/admin')

############################################### DASHBOARD #######################################

#ALL ORDERS ON ADMIN PAGE.
def orders(request):
    if 'logged_admin' not in request.session:
        messages.error(request, "Gotta login bro.")
        return redirect('/adminlogin')
    try:
        pfilter=request.POST['pfilter']
    except:
        pfilter = 'showall'
    if request.method=='GET':
        try:
            orders = Order.objects.filter(billing__bill_first_name__contains=request.GET['search']).order_by("-id") | Order.objects.filter(billing__bill_address1__contains=request.GET['search']).order_by("-id") | Order.objects.filter(status__contains=request.GET['search']).order_by("-id") | Order.objects.filter(total__contains=request.GET['search']).order_by("-id") | Order.objects.filter(id__contains=request.GET['search']).order_by("-id")
        except:
            if pfilter == 'showall':
                orders = Order.objects.all().order_by("-id")
            else:
                orders = Order.objects.filter(status=pfilter).order_by("-id")
    else:
        if pfilter == 'showall':
            orders = Order.objects.all().order_by("-id")
        else:
            orders = Order.objects.filter(status=pfilter).order_by("-id")
    context = {
        'admin': Admin.objects.get(id=request.session['logged_admin']),
        'orders': orders,
        'prod_filter' : pfilter,
    }
    return render(request, 'dope_vinyl/dashboard_allorders.html', context)

def order_status(request, id):
    if request.method=='POST':
        status = request.POST['status']
        Order.objects.filter(id=id).update(status=status)
        return redirect("/dashboard/orders")
    return redirect("/dashboard/orders")

#INDIVIDUAL ORDER ON ADMIN PAGE.
def show_orders(request, id):
   if 'logged_admin' not in request.session:
       messages.error(request, "Gotta login bro")
       return redirect('/adminlogin')
   customerorder = Product_orders.objects.filter(id=id)
   info = Product_orders.objects.filter(orders=id)[0]
   products_in_order = Product_orders.objects.filter(orders=id).annotate(total=Sum(F('products__price') * F('quantity')))
   print products_in_order.query

   totaltotal = 0
   for item in products_in_order:
       price = item.products.price
       quantity = item.quantity
       totaltotal += price * quantity
       print price * quantity
       print item.total
   shiptax = int(7)
   finaltotal = totaltotal + shiptax

   context = {
       'admin' : Admin.objects.get(id=request.session['logged_admin']),
       'customerorder' : customerorder,
       'products_in_order' : products_in_order,
       'shiptax' : shiptax,
       'finaltotal': finaltotal,
       'totaltotal': totaltotal,
       'info': info
   }

   return render(request, 'dope_vinyl/dashboard_showorder.html', context)

#ALL PRODUCTS ON ADMIN PAGE. CLICK ON ADD NEW PRODUCT TO TAKE YOU TO ADD/EDIT ROUTE.

def products(request):
    if 'logged_admin' not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/adminlogin')

    if request.method=='GET':
        try:
            all_products = Product.objects.filter(title__contains=request.GET['search_title']) | Product.objects.filter(artist__name__contains=request.GET['search_title'])
        except:
            all_products = Product.objects.all().order_by('-id')
    else:
        all_products = Product.objects.all().order_by('-id')

    all_genres = Genre.objects.filter()
    total_orders = Product_orders.objects.filter()

    print total_orders.values()

    context = {
        "all_products": all_products,
        "all_genres": all_genres,
    }
    return render(request, 'dope_vinyl/dashboard_allproducts.html', context)

def products_search(request):

    return redirect("/dashboard/products")

def products_add(request):
    if request.method == "POST":
        if request.POST['genre_new'] != "":
            artist_name = Artist.objects.create(name=request.POST['artist'])
            genre_type = Genre.objects.create(genre_type=request.POST['genre_new'])
            Product.objects.create(artist=artist_name, title=request.POST['title'],description=request.POST['description'],genre=genre_type, price=request.POST['price'], inventory=request.POST['inventory'], image=request.FILES['image'])

        elif request.POST['genre'] != "":
            artist_name = Artist.objects.create(name=request.POST['artist'])
            genre_type = Genre.objects.get(genre_type=request.POST['genre'])
            Product.objects.create(artist=artist_name, title=request.POST['title'],description=request.POST['description'],genre=genre_type, price=request.POST['price'], inventory=request.POST['inventory'], image=request.FILES['image'])
    return redirect("/dashboard/products")

def products_edit(request, id):
    if request.method == "POST":
        if request.POST['genre_new'] != "":
            genre_type = request.POST['genre_new']
            Product.objects.filter(id=id).update(title=request.POST['title'],description=request.POST['description'], price=request.POST['price'], inventory=request.POST['inventory'])

        elif request.POST['genre'] != "":
            genre_type = request.POST['genre']
            Product.objects.filter(id=id).update(title=request.POST['title'],description=request.POST['description'], price=request.POST['price'], inventory=request.POST['inventory'])

    return redirect("products")

def products_delete(request, id):
    Product.objects.get(id=id).delete()
    return redirect("/dashboard/products")
