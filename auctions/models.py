from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    cat = models.CharField(max_length=100)

    def __str__(self):
        return self.cat

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid}"

class Listings(models.Model):
    title = models.TextField()
    desc = models.TextField()
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    image = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="listing_bid", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="userwatchlist")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listingcomments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
