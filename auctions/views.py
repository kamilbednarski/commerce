from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Bid, Category, Contact, Comment, Listing, User


def index(request):
    '''
    Renders index page.
    '''
    return render(request, "auctions/index.html")


def login_view(request):
    '''
    Logs user in.
    '''
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("profile"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    '''
    Logs user out.
    '''
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    '''
    Registers new user.
    '''
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            Contact.objects.create(user_id=user.id)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("profile"))
    else:
        return render(request, "auctions/register.html")


@login_required
def profile_view(request):
    '''
    Renders profile page with user data.
    '''
    # Gets data about logged user from User model.
    logged_user = request.user
    id = logged_user.id
    username = logged_user.username
    first_name = logged_user.first_name
    last_name = logged_user.last_name
    email = logged_user.email
    
    # Gets additional data from Contact model.
    contact = Contact.objects.get(user_id=id)
    house = contact.house
    street = contact.street
    post_code = contact.postcode
    city = contact.city
    country = contact.country

    return render(request, "auctions/profile_view.html", {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "house": house,
        "street": street,
        "postcode": post_code,
        "city": city,
        "country": country
    })


@login_required
def change_email(request):
    '''
    Changes email field in User model.
    '''
    if request.method == 'POST':

        # Checks if all form inputs were submited.
        if request.POST["email"] and request.POST["password"] and request.POST["password_confirmation"]:
            email = request.POST["email"]
            password = request.POST["password"]
            confirmation = request.POST["password_confirmation"]
            
            # Checks if password and confirmation are equal.
            if password != confirmation:
                messages.info(request, "Password confirmation do not match password.") 
                return redirect('change_email')

            logged_user = request.user

            # Password authentication.
            check_password = authenticate(request, username=logged_user.username, password=password)

            if check_password is not None:
                # Update and save email field for logged user.
                logged_user.email = email
                logged_user.save()
                messages.info(request, "E-mail succesfully updated.")
                return redirect('profile')
            else:
                # If authentication failed, flashes message and redirects.
                messages.info(request, "Password is uncorrect.") 
                return redirect('change_email')
                
        else:
            # If not all form inputs were submitted, flashes message and redirects.
            messages.info(request, "You must fill in all the fields.") 
            return redirect('change_email')
    else:
        return render(request, "auctions/change_email.html")


@login_required
def change_password(request):
    '''
    Changes password in User model.
    '''
    if request.method == 'POST':

        # Checks if all form inputs were submited.
        if request.POST["new_password"] and request.POST["new_password_confirmation"] and request.POST["password"] and request.POST["password_confirmation"]:
            new_password = request.POST["new_password"]
            new_password_confirmation = request.POST["new_password_confirmation"]
            password = request.POST["password"]
            confirmation = request.POST["password_confirmation"]
            
            # Checks if password and confirmation are equal.
            if password != confirmation or new_password != new_password_confirmation:
                messages.info(request, "Password confirmation(s) do not match password.") 
                return redirect('change_password')

            logged_user = request.user

            # Password authentication.
            check_password = authenticate(request, username=logged_user.username, password=password)

            if check_password is not None:
                # Update and save email field for logged user.
                logged_user.set_password(new_password)
                logged_user.save()
                messages.info(request, "Password succesfully updated. Log in using new password.")
                return redirect('login')
            else:
                # If authentication failed, flashes message and redirects.
                messages.info(request, "Password is uncorrect.") 
                return redirect('change_password')
                
        else:
            # If not all form inputs were submitted, flashes message and redirects.
            messages.info(request, "You must fill in all the fields.") 
            return redirect('change_password')
    else:
        return render(request, "auctions/change_password.html")

@login_required
def profile_edit(request):
    '''
    Changes user data in User and Contact models.
    '''
    if request.method == 'POST':
        # Checks if all form inputs were submited.
        if request.POST["first_name"] or request.POST["last_name"] or request.POST["house"] or request.POST["street"] or request.POST["postcode"] or request.POST["city"] or request.POST["country"]:
            logged_user = request.user
            contact = Contact.objects.get(user_id=logged_user.id)
            
            # If first name was submitted.
            if request.POST["first_name"]:
                logged_user.first_name = request.POST["first_name"]
                logged_user.save()
            # If last name was submitted.
            if request.POST["last_name"]:
                logged_user.last_name = request.POST["last_name"]
                logged_user.save()
            # If house was submitted.
            if request.POST["house"]:
                contact.house = request.POST["house"]
                contact.save()
            # If street was submitted.
            if request.POST["street"]:
                contact.street = request.POST["street"]
                contact.save()
            # If postcode was submitted.
            if request.POST["postcode"]:
                contact.postcode = request.POST["postcode"]
                contact.save()
            # If city was submitted.
            if request.POST["city"]:
                contact.city = request.POST["city"]
                contact.save()
            # If country was submitted.
            if request.POST["country"]:
                contact.country = request.POST["country"]
                contact.save()

            messages.info(request, "Profile succesfully updated.")
            return redirect('profile')
        
        else:
            # If no field was changed, flashes message and redirects.
            messages.info(request, "You must change at least one field.") 
            return redirect('profile_edit')

    else:
        return render(request, "auctions/profile_edit.html")


def categories_view(request):
    '''
    Renders page with all avaiable categories.
    '''
    categories = Category.objects.all().order_by('name')
    print(f"#####{categories}")

    return render(request, "auctions/categories.html", {
        "categories": categories
    })