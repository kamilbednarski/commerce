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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    house = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    postcode = models.CharField(max_length=5)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

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
    date_added = models.DateTimeField(default=timezone.now)
    starting_price = models.FloatField()
    active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Bid(models.Model):
    '''
    Model for listing's bid.
    Contains bid offered and listing ID. 
    '''
    value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return self.value