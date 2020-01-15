from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings

from .models import Product, Profile, Purchase, Review
from .forms import ProductForm


import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                    merchant_id="3hrtz5z44xv9rc5h",
                                    public_key="njnd4544v5q2zd2h",
                                    private_key="604996d1b5f408541a9a34b34a18d373")

# Create your views here.
def home(request):
    products = Product.objects.filter(status=True)
    return render(request, 'index.html', {"products": products})

def product_detail(request, id):
    if request.method == 'POST' and \
        not request.user.is_anonymous() and \
        Purchase.objects.filter(product_id=id, buyer=request.user).count() > 0 and \
        'content' in request.POST and \
        request.POST['content'].strip() != '':
        Review.objects.create(content=request.POST['content'], product_id=id, user=request.user)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return redirect('/')

    if request.user.is_anonymous or \
        Purchase.objects.filter(product=product, buyer=request.user).count() == 0 or \
        Review.objects.filter(product=product, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(product=product, buyer=request.user).count() > 0

    reviews = Review.objects.filter(product=product)
    client_token = braintree.ClientToken.generate()
    return render(request, 'product_detail.html', {"show_post_review": show_post_review ,"reviews": reviews, "product": product, "client_token": client_token})

@login_required(login_url="/")
def create_product(request):
    error = ''
    if request.method == 'POST':
        # file save
        filename = handle_uploaded_file(request.FILES['photo'])
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['photo'] = filename
        request.POST._mutable = mutable
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('my_products')
        else:
            error = "Data is not valid"

    product_form = ProductForm()
    return render(request, 'create_product.html', {"error": error})

@login_required(login_url="/")
def edit_product(request, id):
    try:
        product = Product.objects.get(id=id, user=request.user)
        error = ''
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES, instance=product)
            if product_form.is_valid():
                product.save()
                return redirect('my_products')
            else:
                error = "Data is not valid"

        return render(request, 'edit_product.html', {"product": product, "error": error})
    except Product.DoesNotExist:
        return redirect('/')

@login_required(login_url="/")
def my_products(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'my_products.html', {"products": products})

@login_required(login_url="/")
def profile(request, username):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    else:
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect('/')

    products = Product.objects.filter(user=profile.user, status=True)
    return render(request, 'profile.html', {"profile": profile, "products": products})

@login_required(login_url="/")
def create_purchase(request):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id = request.POST['product_id'])
        except Product.DoesNotExist:
            return redirect('/')

        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": product.price,
            "payment_method_nonce": nonce
        })

        if result.is_success:
            Purchase.objects.create(product=product, buyer=request.user)

    return redirect('/')

@login_required(login_url="/")
def my_sellings(request):
    purchases = Purchase.objects.filter(product__user=request.user)
    return render(request, 'my_sellings.html', {"purchases": purchases})

@login_required(login_url="/")
def my_buyings(request):
    purchases = Purchase.objects.filter(buyer=request.user)
    return render(request, 'my_buyings.html', {"purchases": purchases})

def category(request, link):
    categories = {
        "AR": "Arabica",
        "RB": "Robusta",
    }
    try:
        products = Product.objects.filter(category=categories[link])
        return render(request, 'index.html', {"products": products})
    except KeyError:
        return redirect('home')

def search(request):
    products = Product.objects.filter(title__contains=request.GET['title'])
    return render(request, 'index.html', {"products": products})
def search_page(request):
    products = Product.objects.filter(status=True)
    return render(request, 'search.html', {"products": products})

#login
def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "user.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect(reverse("index"))
            # return HttpResponse("User logged in")
            return redirect('home')
            # products = Product.objects.filter(status=True)
            # return render(request, 'index.html', {"products": products})
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    # return render(request, "login.html", {"message": "Logged out."})
    products = Product.objects.filter(status=True)
    return render(request, 'index.html', {"products": products})
def sign_up(request):
    return render(request, 'sign_up.html')



# file handle
def handle_uploaded_file(f):
    with open(settings.FILE_UPLOAD_DIR + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return f.name