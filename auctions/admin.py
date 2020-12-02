from django.contrib import admin

from .models import Bid, Category, Contact, Comment, Listing, User

# Register your models here.
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(User)
