from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from django.conf import settings

from django.core.serializers import serialize
import json, stripe, datetime
from .models import *
from .forms import *
from django.db.models import Avg, Count


# admin check
def admin_check(user):
    return user.is_staff

rate_dict = {
    "kurta" : {"rate" : KurtaRate, "size" : KurtaSize },
    "top" : {"rate" : TopRate, "size" : TopSize },
    "trouser" : {"rate" : TrouserRate, "size" : TrouserSize },
    "saree" : {"rate" : SareeRate, "size" : SareeSize }
    }

def sort_order(sort):
    kurtarate = KurtaRate.objects.order_by(sort)
    toprate = TopRate.objects.order_by(sort)
    trouserrate = TrouserRate.objects.order_by(sort)
    sareerate = SareeRate.objects.order_by(sort)
    return kurtarate, toprate, trouserrate, sareerate

def recently_added_dresses():
    recently_added = {}
    recently_added["kurta"] = json.loads(serialize("json", KurtaRate.objects.order_by('-pk')[:4]))
    recently_added["top"] = json.loads(serialize("json",TopRate.objects.order_by('-pk')[:4]))
    recently_added["trouser"] = json.loads(serialize("json",TrouserRate.objects.order_by('-pk')[:4]))
    recently_added["saree"] = json.loads(serialize("json",SareeRate.objects.order_by('-pk')[:4]))
    return recently_added

def incart_items(request):
    items = DressOrder.objects.filter(user = request.user, paid = False)
    return items

def add_paid_orders(request,address_to_delivery):
    try:
        items = incart_items(request)
        total_cost = 0
        for item in items:
            item.paid = True
            item.save()
            total_cost += rate_dict[item.dresstype]['rate'].objects.get(pk = item.dresspk).price
        placedorder = PlacedOrder(user = request.user, deliveryaddress = DeliveryAddress.objects.get(pk = address_to_delivery), total = total_cost)
        placedorder.save()
        placedorder.order.set(items)
        placedorder.save()
        return "success"
    except:
        return "failure"

# Create your views here.
def index(request):
    context = {"incart_items" : len(incart_items(request))}
    # testing form
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for f in files:
            fileupload = Document(document = f)
            fileupload.save()
        context = {"test" : fileupload.document.url,"incart_items" : len(incart_items(request))}
    else:
        pass
    return render(request, "shopping/index.html", context)

def collections(request):
    sort = '-pk'
    if request.method == "POST":
        todo = request.POST['todo']
        if todo == "sort":
            sort = request.POST['sortinput']
        elif todo == "deleteitem":
            dresspk = request.POST['dresspk']
            dresstype = request.POST['dresstype']
            dress = rate_dict[dresstype]['rate'].objects.get(pk = dresspk)
            dress.delete()
    kurtarate, toprate, trouserrate, sareerate = sort_order(sort)
    if request.user.id:
        incart_item = len(incart_items(request))
    else:
        incart_item = None
    context = {
    "currency" : rupees,
    "kurtarate" : kurtarate,
    "toprate" : toprate,
    "trouserrate" : trouserrate,
    "sareerate" : sareerate,
    "incart_items" : incart_item
    }
    return render(request, "shopping/collections.html", context)

@login_required(login_url='/login')
def histories(request):
    status = None
    if request.method == "POST":
        stripe.api_key = "sk_test_tSFhKEyCfNka1V4A71VZWbWc"
        token = request.POST['stripeToken']
        amount = request.POST['amount']
        address_to_delivery = request.POST['address_to_delivery']
        try:
            charge = stripe.Charge.create( amount=int(amount), currency='inr', description='charge', source=token)
            status = "success"
            add_paid_orders(request, address_to_delivery);
        except Exception as e:
            status = str(e)
    placed_orders = PlacedOrder.objects.filter(user = request.user).order_by('-pk')
    context = {
    "kurtarate" : rate_dict['kurta']['rate'].objects.all(),
    "toprate" : rate_dict['top']['rate'].objects.all(),
    "trouserrate" : rate_dict['trouser']['rate'].objects.all(),
    "sareerate" : rate_dict['saree']['rate'].objects.all(),
    "placed_orders" : placed_orders,
    "status" : status
    }
    return render(request, "shopping/histories.html", context)

@login_required(login_url='/login')
def cart(request):
    if request.method == "POST":
        todo = request.POST['todo']
        if todo == "delete":
            orderpk = request.POST['orderpk']
            removeorder = DressOrder.objects.get(pk = orderpk)
            removeorder.delete()
        elif todo == "address":
            new_address = request.POST['new_address']
            new_number = request.POST['new_number']
            address = DeliveryAddress(user = request.user, address = new_address, phone_number = new_number)
            address.save()
        return HttpResponseRedirect(reverse("cart"))
    userorders = DressOrder.objects.filter(user = request.user, paid = False).order_by('-pk')
    userorder_list = []
    total_cost = 0
    for userorder in userorders:
        order = rate_dict[userorder.dresstype]['rate'].objects.get(pk = userorder.dresspk)
        size = rate_dict[userorder.dresstype]['size'].objects.get(pk = userorder.sizepk)
        orderpk = userorder.pk
        userorder_list.append((order, size, orderpk))
        total_cost += order.price
    context = {
        "deliveryaddress" : DeliveryAddress.objects.filter(user = request.user).order_by('-pk'),
        "total_cost" : total_cost,
        "currency" : rupees,
        "userorder_list" : userorder_list
    }
    return render(request, "shopping/cart.html", context)

@login_required(login_url='/login')
def dressitem(request, dress_type, dress_id):
    if not dress_type in rate_dict.keys():
        return render(request, "shopping/index.html", {"message" : "Unknown URL path", "incart_items" : len(incart_items(request))})
    try:
        dress = rate_dict[dress_type]['rate'].objects.get(pk = dress_id)
        dresssize = rate_dict[dress_type]['size'].objects.all()
        dresscolor_obj = rate_dict[dress_type]['rate'].objects.filter(model = dress.model)
    except:
        return render(request, "shopping/index.html", {"message" : "Requested item does not exist"})
    context = {
        "range" : range(1,6),
        "currency" : rupees,
        "dresscolor_obj" : dresscolor_obj,
        "dresssize" : dresssize,
        "dress" : dress,
    }
    if request.method == "POST":
        todo = request.POST['todo']
        dresspk = request.POST['dresspk']
        dresstype = request.POST['dresstype']
        if todo == 'add':
            sizepk = request.POST['sizepk']
            addorder = DressOrder(user = request.user, dresstype = dresstype, dresspk = dresspk, sizepk = sizepk)
            addorder.save()
        elif todo == 'deleteitem':
            dress = rate_dict[dresstype]['rate'].objects.get(pk = dresspk)
            dress.delete()
            return HttpResponseRedirect(reverse("collections"))
        else:
            x=0
            try:
                user_input = UserInput.objects.filter(user = request.user, dresspk = dresspk, dresstype = dresstype).first()
                if not user_input:
                    x=1
                    raise ValueError
            except:
                user_input = UserInput(user = request.user, dresspk = dresspk, dresstype = dresstype)
                user_input.save()
            if todo == "rate":
                rating_input = request.POST['rating_input']
                user_input.rating = rating_input
            elif todo == "review":
                review_input = request.POST['reviewinput']
                user_input.review = review_input
            elif todo == "delete_review":
                user_input.review = None
            user_input.save()
    context["currentuserinput"] = UserInput.objects.filter(dresspk = dress_id, user = request.user).first()
    context["userinput"] = UserInput.objects.filter(dresspk = dress_id).order_by('-pk')
    context["overall_rating"] = UserInput.objects.filter(dresspk = dress_id).aggregate(Avg("rating"))
    context["overall_rating_count"] = UserInput.objects.filter(dresspk = dress_id).aggregate(Count("rating"))
    context["incart_items"] = len(incart_items(request))
    return render(request, "shopping/dressitem.html", context)

@login_required(login_url='/login')
@user_passes_test(admin_check)
def additems(request):
    context = {
        "currency" : rupees,
        "image" : serialize("json", Document.objects.all()),
        "color" : serialize("json", Color.objects.get_queryset()),
        "sareesize" : serialize("json", SareeSize.objects.get_queryset()),
        "trousersize" : serialize("json", TrouserSize.objects.get_queryset()),
        "topsize" : serialize("json", TopSize.objects.get_queryset()),
        "kurtasize" : serialize("json", KurtaSize.objects.get_queryset())
    }
    if request.method == "POST":
        todo = request.POST['todo']
        if todo == "additem":
            dresstype = request.POST['dresstype']
            dressname = request.POST[f"t_{dresstype}name"]
            dressmodel = request.POST[f"t_{dresstype}model"]
            # dresssize = request.POST[f"{dresstype}size"]
            dresssize = request.POST[f"t_{dresstype}size"]
            dresssize = dresssize.split(",")
            dresscolor = request.POST[f"{dresstype}color"]
            dressprice = request.POST[f"p_{dresstype}"]
            images = request.FILES.getlist(f"i_{dresstype}image")
            uploaded_images = []
            for i in images:
                upload = Document(document = i, color = Color.objects.get(code = dresscolor))
                upload.save()
                uploaded_images.append(upload)
            # return HttpResponse(str(uploaded_images))
            # adding to rate ORM
            dressrate_obj = rate_dict[dresstype]['rate']
            dresssize_obj = rate_dict[dresstype]['size']
            dresssize_list = [dresssize_obj.objects.get(pk = d) for d in dresssize]
            dress = dressrate_obj(name = dressname, model = dressmodel, price = dressprice)
            dress.save()
            if dresssize_list:
                dress.size.set(dresssize_list)
                dress.save()
            if uploaded_images:
                dress.image.set(uploaded_images)
                dress.save()
        return HttpResponseRedirect(reverse("additems"))
    # recently added
    context["recently_added"] = recently_added_dresses()
    context["incart_items"] = len(incart_items(request))
    return render(request, "shopping/additems.html", context)


# login/registration
# check email function
import re
def check_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "shopping/index.html", {"message" : "User already logged in"})
        else:
            return render(request, "shopping/login.html", {"message" : None})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "shopping/login.html", {"message" : "Invalid credentials"})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return render(request, "shopping/login.html", { "message" : "Logged out successfully"})

def register_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "shopping/index.html", {"message" : "User already logged in"})
        else:
            return render(request, "shopping/register.html", {"message" : None})
    else:
        username = request.POST["username"]
        useremail = request.POST["useremail"]
        password = request.POST["password"]
        password_retype = request.POST["password_retype"]
        userlist = [u.username for u in User.objects.all()]
        if username in userlist:
            return render(request, "shopping/register.html", {"message" : "User already exist"})
        if password == password_retype and check_email(useremail):
            try:
                user = User.objects.create_user(username, useremail, password)
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            except:
                return render(request, "shopping/register.html", {"message" : "Error in user registration"})
        else:
            return render(request, "shopping/register.html", {"message" : "Check user credentials"})
