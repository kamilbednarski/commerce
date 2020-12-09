from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files import File

from .models import Bid, Category, Contact, Comment, Listing, User, Watchlist


def index(request):
    '''
    Renders page with all active listings.
    '''
    # Gets all Listing objects.
    listings = Listing.objects.all().order_by('-date_added')
    # Gets all Category objects.
    categories = Category.objects.all().order_by('name')
    
    header_title = "All listings"

    return render(request, "auctions/browse_listings.html", {
        "listings": listings,
        "categories": categories,
        "header_title": header_title,
        "logged_user_id": "No winner"
    })


def categories_view(request):
    '''
    Renders page with all avaiable categories.
    '''
    # Gets all Category objects.
    categories = Category.objects.all().order_by('name')

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def single_listing_view(request, id):
    '''
    Renders page for single listing.
    '''
    logged_user = request.user
    
    try:
        watchlist = Watchlist.objects.get(user_id=logged_user.id, listing_id=id)
    except Watchlist.DoesNotExist:
        watchlist = None

    listing = Listing.objects.get(id=id)
    comments = Comment.objects.filter(listing_id=id)

    user_ids = []
    for comment in comments:
        user_ids.append(comment.author_id)

    user_ids = set(user_ids)

    authors = User.objects.filter(id__in=user_ids)

    return render(request, "auctions/listing_single_view.html", {
        "logged_user_id": logged_user.id,
        "listing": listing,
        "comments": comments,
        "authors": authors,
        "watchlist": watchlist
    })


def browse_listings_category(request):
    '''
    Renders page with all active listings matching selected category.
    '''
    if request.method == 'POST':
        # TODO check if int() function necessary
        category_id = int(request.POST['category_id'])
        category = Category.objects.get(id=category_id)

        # Gets listings from Listing objects with matching category_id.
        listings = Listing.objects.filter(category_id=category_id).order_by('-date_added')

        return render(request, "auctions/browse_listings_category.html", {
            "listings": listings,
            "category": category
        })

    else:
        return redirect('categories_view')


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



'''
USER SPECIFIC, LOGIN REQUIRED FUNCTIONALITY
'''


@login_required
def logout_view(request):
    '''
    Logs user out.
    '''
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        # Checks if form inputs were submited.
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


@login_required
def add_listing(request):
    '''
    Allows logged user to add new listing.
    '''
    if request.method == 'POST':
        # Checks if all form inputs were submited.
        if request.POST["title"] and request.POST["description"] and request.POST["price"] and request.POST["category"]:
            logged_user = request.user

            # Saves data about new listing provided in html form.
            title = request.POST["title"]
            description = request.POST["description"]
            starting_price = float(request.POST["price"])
            current_price = float(request.POST["price"])
            user_id = logged_user.id

            # Gets category id from Category object.
            post_category = request.POST["category"]

            # Get category with id equal to id from POST method.
            category = Category.objects.get(id=post_category)

            # Checks if category is correct.
            if category:
                category_id = category.id

                if request.FILES["image"]:
                    photo = request.FILES["image"]
                    # Creates new Listing instance.
                    new_listing = Listing(title=title, description=description, starting_price=starting_price, current_price=current_price, photo=photo, user_id=user_id, category_id=category_id)

                else:
                    # Creates new Listing instance.
                    new_listing = Listing(title=title, description=description, starting_price=starting_price, user_id=user_id, category_id=category_id)
                
                new_listing.save()

                return redirect('index')
            
            else:
                # If category not valid, redirect.
                messages.info(request,"Such listing category does not exist.")
                return redirect('add_listing')

        else:
            # If not, redirect and flash message.
            messages.info(request, "You must fill all fields.") 
            return redirect('add_listing')

    else:
        # Renders page with form.
        categories = Category.objects.all().order_by('name')

        return render(request, "auctions/add_listing.html", {
            "categories": categories
        })


@login_required
def listings_view(request):
    '''
    Renders page with all active listings created by logged user.
    '''
    logged_user = request.user
    user_id = logged_user.id

    # Gets listings from Listing objects with matching user_id.
    listings = Listing.objects.filter(user_id=user_id).order_by('-date_added')
    categories = Category.objects.all().order_by('name')

    return render(request, "auctions/listings_view.html", {
        "listings": listings,
        "categories": categories
    })


@login_required
def listing_delete(request):
    '''
    Allows logged user to delete listings which user created.
    '''
    if request.method == 'POST':
        logged_user = request.user
        user_id = logged_user.id

        # Gets listing id from POST method.
        # and searches for Listing object with that id.
        listing_id = request.POST['listing_id']
        listing = Listing.objects.get(id=listing_id)

        if listing.user_id == user_id:
            listing.delete()
        return redirect('listings_view')

    else:
        return redirect('listings_view')

@login_required
def listing_deactivate(request):
    '''
    Allows user to deactivate listing.
    '''
    if request.method == 'POST':
        logged_user = request.user
        user_id = logged_user.id

        # Gets listing id from POST method.
        # and searches for Listing object with that id.
        listing_id = request.POST['listing_id']
        listing = Listing.objects.get(id=listing_id)

        if listing.user_id == user_id:
            listing.active = 0
            listing.save()
        return redirect('listings_view')

    else:
        return redirect('listings_view')


@login_required
def listing_activate(request):
    '''
    Allows user to activate listing.
    '''
    if request.method == 'POST':
        logged_user = request.user
        user_id = logged_user.id

        # Gets listing id from POST method.
        # and searches for Listing object with that id.
        listing_id = request.POST['listing_id']
        listing = Listing.objects.get(id=listing_id)

        if listing.user_id == user_id:
            listing.active = 1
            listing.save()
        return redirect('listings_view')

    else:
        return redirect('listings_view')


@login_required
def listing_end(request):
    '''
    Allows user to end his listing.
    By using this method, user with highest bid
    automatically becomes winner for that listing.
    '''
    if request.method == 'POST':
        logged_user = request.user
        user_id = logged_user.id

        # Gets listing id from POST method.
        # and searches for Listing object with that id.
        listing_id = request.POST['listing_id']
        listing = Listing.objects.get(id=listing_id)

        # Gets bid with matching listing_id and value.
        bid = Bid.objects.get(listing_id=listing.id, value=listing.current_price)
       
        # Listing winner gets user id from matching bid.
        listing.winner = bid.user_id
        listing.active = 0
        listing.save()

        winner = User.objects.get(id=listing.winner)
        
        messages.info(request, f"Auction succesfully closed. Winner of this auction is {winner.username}.")
        return redirect('listings_view')

    else:
        return redirect('listings_view')


@login_required
def add_reply(request):
    '''
    Allows logged user who's also listing's author
    to add reply to public comment.
    '''
    if request.method == 'POST':
        if request.POST['comment_id'] and request.POST['reply_content'] and request.POST['listing_id']:
            # Saves data from POST method.
            comment_id = request.POST['comment_id']
            reply_content = request.POST['reply_content']
            listing_id = request.POST['listing_id']

            # Gets comment object with matching id.
            comment = Comment.objects.get(id=comment_id)
            comment.reply = reply_content
            comment.save()
            
            # After adding reply field to comment object, redirects to listing view.
            messages.info(request, 'Reply added successfully.')
            return redirect('single_listing_view', listing_id)

        else:
            listing_id = request.POST['listing_id']
            messages.info(request, 'You cannot post empty reply.')
            return redirect('single_listing_view', listing_id)

    else:
        return redirect('index')


@login_required
def add_comment(request):
    '''
    Allows logged user to add public comment
    to any listing that does not belong to that user.
    '''
    if request.method == 'POST':
        if request.POST['listing_id'] and request.POST['comment_content'] and request.POST['comment_author']:
            # Saves data from POST method.
            listing_id = request.POST['listing_id']
            # Gets Listing object with matching id.
            listing = Listing.objects.get(id=listing_id)
            
            comment_author_id = request.POST['comment_author']
            # Gets User object with matching id.
            comment_author = User.objects.get(id=comment_author_id)

            comment_content = request.POST['comment_content']

            # Creates new Comment object.
            comment = Comment(content = comment_content, listing = listing, author = comment_author)
            comment.save()

            # After adding reply field to comment object, redirects to listing view.
            messages.info(request, 'Comment added successfully.')
            return redirect('single_listing_view', listing_id)

        else:
            listing_id = request.POST['listing_id']
            messages.info(request, 'You cannot post empty comment.')
            return redirect('single_listing_view', listing_id)

    else:
        return redirect('index')


@login_required
def add_bid(request):
    '''
    Allows logged user to add bid to any listing
    that does not belong to that user.
    '''
    if request.method == 'POST':
        if request.POST['bid_value'] and request.POST['listing_id']:
            # Saves data from POST method.
            value = float(request.POST['bid_value'])
            listing_id = request.POST['listing_id']

            # Gets logged user.
            logged_user = request.user

            # Gets Listing object with matching id.
            listing = Listing.objects.get(id=listing_id)
            current_price = listing.current_price
            # Checks if new bid is higher than current price.
            if value > current_price:
                # Updates current price of listing.
                listing.current_price = value
                listing.save()
                # Creates new Bid object.
                bid = Bid(value = value, user = logged_user, listing = listing)
                bid.save()

                messages.info(request, 'Bid succesfully added.')
                return redirect('single_listing_view', listing_id)

            else:
                messages.info(request, 'New bid has to be higher than current price.')
                return redirect('single_listing_view', listing_id)

        else:
            listing_id = request.POST['listing_id']
            messages.info(request, 'You cannot post empty bid.')
            return redirect('single_listing_view', listing_id)

    else:
        return redirect('index')


@login_required
def add_to_watchlist(request):
    '''
    Allows logged user to add listing to watchlist.
    '''
    if request.method == 'POST':
        if request.POST['listing_id']:
            logged_user = request.user
            listing_id = request.POST['listing_id']
            listing = Listing.objects.get(id = listing_id)

            # Creates watchlist object with connection to provided user and listing.
            new_watchlist = Watchlist(user = logged_user, listing = listing)
            new_watchlist.save()

            messages.info(request, 'Item successfully added to watchlist.')
            return redirect('single_listing_view', listing_id)

        else:
            messages.info(request, 'Error: Listing id must be provided.')
            return redirect('index') 

    else:
        return redirect('index')


@login_required
def remove_from_watchlist(request):
    '''
    Allows logged user to remove listing from watchlist.
    '''
    if request.method == 'POST':
        if request.POST['listing_id']:
            logged_user = request.user
            listing_id = request.POST['listing_id']
            listing = Listing.objects.get(id = listing_id)

            # Gets watchlist object with matching user id and listing id.
            watchlist = Watchlist.objects.get(user_id = logged_user.id, listing_id = listing_id)
            # Deletes selectec watchlist object.
            watchlist.delete()

            messages.info(request, 'Item successfully removed from watchlist.')
            return redirect('single_listing_view', listing_id)

        else:
            messages.info(request, 'Error: Listing id must be provided.')
            return redirect('index') 

    else:
        return redirect('index')


@login_required
def watchlist_view(request):
    '''
    Allows logged user to view listings added to watchlist.
    '''
    logged_user = request.user
    watchlist = Listing.objects.filter(watchlist__user=logged_user).order_by('title') #relationship query

    # Get watchlist
    # Get listings with user_id matching logged user and that are on watchlist
    # Render template with list of listings limited by those filters

    categories = Category.objects.all().order_by('name')
    header_title = "My watchlist"

    return render(request, "auctions/browse_listings.html", {
        "listings": watchlist,
        "categories": categories,
        "header_title": header_title,
        "logged_user_id": str(logged_user.id)
    })