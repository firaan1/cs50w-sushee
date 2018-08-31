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

# admin check
def admin_check(user):
    return user.is_staff

rate_dict = {
    "kurta" : {"rate" : KurtaRate, "size" : KurtaSize },
    "top" : {"rate" : TopRate, "size" : TopSize },
    "trouser" : {"rate" : TrouserRate, "size" : TrouserSize },
    "saree" : {"rate" : SareeRate, "size" : SareeSize }
    }

def recently_added_dresses():
    recently_added = {}
    recently_added["kurta"] = json.loads(serialize("json", KurtaRate.objects.order_by('-pk')[:4]))
    recently_added["top"] = json.loads(serialize("json",TopRate.objects.order_by('-pk')[:4]))
    recently_added["trouser"] = json.loads(serialize("json",TrouserRate.objects.order_by('-pk')[:4]))
    recently_added["saree"] = json.loads(serialize("json",SareeRate.objects.order_by('-pk')[:4]))
    return recently_added

# Create your views here.
def index(request):
    context = {}
    # testing form
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for f in files:
            fileupload = Document(document = f)
            fileupload.save()
        context = {"test" : fileupload.document.url}
    else:
        pass
    return render(request, "shopping/index.html", context)

def order(request):
    context = {}
    return render(request, "shopping/order.html", context)

def dressitem(request, dress_type, dress_id):
    if not dress_type in rate_dict.keys():
        return render(request, "shopping/index.html", {"message" : "Unknown URL path"})
    try:
        dress = rate_dict[dress_type]['rate'].objects.get(pk = dress_id)
        dresssize = rate_dict[dress_type]['size'].objects.all()
        dresscolor_obj = rate_dict[dress_type]['rate'].objects.filter(model = dress.model)
    except:
        return render(request, "shopping/index.html", {"message" : "Requested item does not exist"})
    context = {
        "currency" : rupees,
        "dresscolor_obj" : dresscolor_obj,
        "dresssize" : dresssize,
        "dress" : dress
    }
    return render(request, "shopping/dressitem.html", context)

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
    return render(request, "shopping/additems.html", context)

def model_form_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm2(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(document = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('model_form_upload'))
            context = {"test" : newdoc.document.url}
            return render(request, "shopping/index.html", context)
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request,
        'shopping/model_form_upload.html',
        {'documents': documents, 'form': form})



# file upload
# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             context = {"message" : "upload successful", "form" : form}
#         else:
#             context = {"message" : "upload failed", "form" : form}
#     else:
#         form = DocumentForm()
#         context = {"message" : None, "form" : form}
#     return render(request, "shopping/index.html", context)

# login/registration
# check email function
import re
def check_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
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
