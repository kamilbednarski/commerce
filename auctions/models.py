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

    info = f'Contact card id: {id}'
    
    def __str__(self):
        return self.info

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
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    starting_price = models.FloatField()
    # Connection with User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


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
    # Connection with Listing
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    # Connection with User
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


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
        return self.value