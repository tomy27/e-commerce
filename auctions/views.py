from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listings, Bids, Comments


def index(request):
    if request.method == "POST":
        if request.POST["category"] == "All":
            return render(request, "auctions/index.html", {
            "listings": Listings.objects.filter(isActive=True),
            "pagetitle": "Active Listings"
            })
        category = Category.objects.get(cat=request.POST["category"])
        return render(request, "auctions/index.html", {
            "listings": Listings.objects.filter(category=category, isActive=True),
            "pagetitle": "Active Listings"
        })

    # GET
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(isActive=True),
        "pagetitle": "Active Listings"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

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
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "POST":
            title = request.POST["title"]
            desc = request.POST["desc"]
            image = request.POST["image"]
            start_price = request.POST["start_price"]
            category = Category.objects.get(cat=request.POST["category"])
            user = request.user

            # Save new listing
            new = Listings(title=title, desc=desc, listed_by=user, image=image, isActive=True, start_price=start_price, category=category)
            new.save()

            return redirect("index")

    # GET
    return render(request, "auctions/create.html", {
        "category": Category.objects.all()
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def listings(request, id):
    # Get current price/bid
    listing = Listings.objects.get(id=id)
    if listing.bid is None:
        current_bid = 0
    else:
        current_bid = listing.bid

    # Check if listing is on watchlist
    if request.user in listing.watchlist.all():
        watchlisted = True
    else:
        watchlisted = False

    # Render page
    return render(request, "auctions/listings.html", {
        "listing": Listings.objects.get(id=id),
        "bid": current_bid,
        "watchlisted": watchlisted,
        "comments": Comments.objects.filter(listing=listing)
    })


def bids(request):
    if request.method == "POST":
        # Save the new bid
        new_bid = float(request.POST["bid"])
        item = Listings.objects.get(id=request.POST["item"])
        if item.isActive == False:
            return redirect("index")
        if item.bid is None:
            current_bid = 0
        else:
            current_bid = item.bid.bid

        # Automatically add to watchlist because of bid
        #item.watchlist.add(request.user)

        # Check if listing is on watchlist
        if request.user in item.watchlist.all():
            watchlisted = True
        else:
            watchlisted = False

        if current_bid is None and new_bid >= item.start_price or new_bid >= item.start_price and new_bid > current_bid:
            bid = Bids(user=request.user, bid=new_bid)
            bid.save()
            item.bid = bid
            item.save()

            # Render page with success
            return render(request, "auctions/listings.html", {
                "listing": item,
                "bid": format(new_bid, '.2f'),
                "watchlisted": watchlisted,
                "message": "Success!",
                "comments": Comments.objects.filter(listing=item)
            })
        else:
            # Render page with error
            return render(request, "auctions/listings.html", {
                "listing": item,
                "bid": current_bid,
                "watchlisted": watchlisted,
                "message": "Failed! Bid must be higher than current bid or minimum price.",
                "comments": Comments.objects.filter(listing=item)
            })


def watchlistHandler(request, id):
    if request.method == "POST":
        if request.POST["action"] == "Add":
            list = Listings.objects.get(id=id)
            user = request.user
            list.watchlist.add(user)
        elif request.POST["action"] == "Remove":
            list = Listings.objects.get(id=id)
            user = request.user
            list.watchlist.remove(user)

    # Reload page
    return redirect("listings", id)


def watchlist(request):
    if request.method == "GET":
        return render(request, "auctions/index.html", {
            "listings": User.objects.get(username=request.user).userwatchlist.all(),
            "pagetitle": "Watchlist"
        })


def closeAuction(request):
    if request.method == "POST":
        id = request.POST["item"]
        listing = Listings.objects.get(id=id)
        listing.isActive = False
        listing.save()
        return redirect("index")


def comment(request):
    if request.method == "POST":
        listing = Listings.objects.get(id=request.POST["item"])
        new_comment = Comments(listing=listing, user=request.user, comment=request.POST["comment"])
        new_comment.save()
        return redirect("listings", request.POST["item"])

