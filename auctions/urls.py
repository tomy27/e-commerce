from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("bids", views.bids, name="bids"),
    path("watchlisthandler/<int:id>", views.watchlistHandler, name="watchlistHandler"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closeauction", views.closeAuction, name="closeAuction"),
    path("comment", views.comment, name="comment"),
]
