from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile_view, name="profile"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
    path("profile/change/email", views.change_email, name="change_email"),
    path("profile/change/password", views.change_password, name="change_password"),
    path("add", views.add_listing, name="add_listing"),
    path("category", views.categories_view, name="categories_view"),
    path("browse", views.browse_listing, name="browse_listing")
]