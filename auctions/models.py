import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass


class Contact(models.Model):
    '''
    Model for user's contact data.
    Contains full name, email, house nr,
    street, postcode, city and country.
    '''
    house = models.CharField(max_length=64, blank=True, null=True)
    street = models.CharField(max_length=64, blank=True, null=True)
    postcode = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_username(self):
        user = User.objects.get(id=self.user_id)
        username = user.username
        return username

    def __str__(self):
        return "Contact card for: " + str(self.get_username())


class Category(models.Model):
    '''
    Model for listing's category.
    Contains name of category.
    '''
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Listing(models.Model):
    '''
    Model for listing.
    Each listing is connected with one user.
    Contains title, description, date added,
    starting price and status field(active/not active).
    '''
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    starting_price = models.FloatField()
    current_price = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='listing_images', default='default.jpg')
    # Connection with User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=30, blank=True, null=True)

    def get_status(self):
        if self.active == 1:
            return "active"
        else:
            return "not active"

    def get_id(self):
        return self.id

    def get_username(self):
        user = User.objects.get(id=self.user_id)
        username = user.username
        return username

    def get_winner_username(self):
        if self.winner:
            user = User.objects.get(id=self.winner)
            username = user.username
            return username

    def __str__(self):
        return "Listing with id: " + str(self.get_id()) + " assigned author: " + str(self.get_username()) + " title: " + self.title


class Comment(models.Model):
    '''
    Model for comment.
    Comment is assigned to author(user)
    and listing.
    Contains date added, comment content,
    affiliation to listing and author's ID.
    '''
    date_added = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=140)
    reply = models.CharField(max_length=140, blank=True, null=True)
    # Connection with Listing
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    # Connection with User
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_id(self):
        return self.id

    def get_listing_id(self):
        return self.listing_id

    def get_listing_author_username(self):
        listing = Listing.objects.get(id=self.listing_id)
        listing_author_id = listing.user_id
        author = User.objects.get(id=listing_author_id)
        username = author.username
        return username

    def __str__(self):
        return "Comment for listing of id: " + str(self.get_listing_id()) + " of author: " + str(self.get_listing_author_username())


class Bid(models.Model):
    '''
    Model for listing's bid.
    Contains bid offered and listing ID. 
    '''
    value = models.FloatField()
    # Connection with User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Connection with Listing
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        listing = str(self.listing)
        value = str(self.value)
        self_description = listing + " bid value: " + value
        return self_description


class Watchlist(models.Model):
    '''
    Model for user's wishlist positions.
    Contains listing id and user id.
    '''
    # Connection with User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Connection with Listing
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def get_username(self):
        user = User.objects.get(id=self.user_id)
        return user.username

    def __str__(self):
        return "Position in watchlist of user: " + str(self.get_username())