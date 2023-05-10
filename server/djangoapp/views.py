from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from urllib.request import urlopen
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context ={}
    if request.method == 'GET':
        return render(request, "djangoapp/about.html", context)

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            print("logging in {} with password {}".format(username, password))
            login(request, user)
            return redirect('djangoapp:logged_in')
        else:
            # If not, return to login page again
            print("logging in {} with password {} FAILED".format(username, password))
            context["error"] = "Authentication failed."
    else:
        context["error"] = "Malformed request."

    return render(request, 'djangoapp/login.html', context)

def logged_in(request):
    return render(request, "djangoapp/logged_in.html")

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:logout_final')

def logout_final(request):
    return render(request, "djangoapp/logout.html")

def contact(request):
    context ={}
    if request.method == 'GET':
        return render(request, "djangoapp/contact.html", context)

def registration(request):
    context ={}
    if request.method == 'GET':
        return render(request, "djangoapp/registration.html", context)

def register_request(request):
    context ={}
    username = request.POST["username"]
    password1, password2 = request.POST["password1"], request.POST["password2"]
    if request.method == 'POST':
        if password1 == password2:
            if find_user(username) == None :
                now = datetime.now()
                nowstr = "{}-{}-{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute)
                u= User.objects.create_user(username, request.POST["email"], password1)
                u.first_name =request.POST["first_name"]
                u.last_name=request.POST["last_name"]
                u.last_login = u.date_joined = now
                u.save()
                return render(request, "djangoapp/about.html", context)
            else:
                context["error"]="User already exists"
        else:
            context["error"] = "Passwords don't match."
    else:
        context["error"] = "Invalid request method"
    return render(request, "djangoapp/registration.html", context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    context["dealers"] = get_dealers_from_cf(
        "https://us-south.functions.appdomain.cloud/api/v1/web/e29a6e0e-0353-4f6d-9381-7d24deb6529f/dealership-package/dealership")
    return HttpResponse(
        "<br>".join([dealer.short_name for dealer in context["dealers"]]))
def get_reviews_for_dealer(request, dealer_id):
    context = {}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/e29a6e0e-0353-4f6d-9381-7d24deb6529f/dealership-package/review?dealershipId="
    url += str(dealer_id)
    context["reviews"] = get_dealer_reviews_from_cf(url, request=request)
    return HttpResponse(
        "<br>".join([review.review for review in context["reviews"]]))

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/e29a6e0e-0353-4f6d-9381-7d24deb6529f/dealership-package/review?dealershipId="
    url += str(dealer_id)
    response = urlopen(url)
    data_json = json.loads(response.read())
    print(data_json)
    context = data_json[0]
    return render(request, "djangoapp/dealer_details.html", context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def find_user(username):
    try:
        return User.objects.get(username=username)
    except:
        return None
