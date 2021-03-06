from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<str:id>", views.single_listing_view, name="single_listing_view"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("profile", views.profile_view, name="profile"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
    path("profile/change/email", views.change_email, name="change_email"),
    path("profile/change/password", views.change_password, name="change_password"),
    path("profile/view/mylistings", views.listings_view, name="listings_view"),
    path("profile/view/mylistings/delete", views.listing_delete, name="listing_delete"),
    path("profile/view/mylistings/deactivate", views.listing_deactivate, name="listing_deactivate"),
    path("profile/view/mylistings/activate", views.listing_activate, name="listing_activate"),
    path("profile/view/mylistings/end", views.listing_end, name="listing_end"),

    path("watchlist/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/browse", views.watchlist_view, name="watchlist_view"),

    path("add", views.add_listing, name="add_listing"),

    path("category", views.categories_view, name="categories_view"),
    path("category/browse", views.browse_listings_category, name="browse_listings_category"),

    path("comment/reply", views.add_reply, name="add_reply"),
    path("comment/add", views.add_comment, name="add_comment"),
    path("bid/add", views.add_bid, name="add_bid")
]