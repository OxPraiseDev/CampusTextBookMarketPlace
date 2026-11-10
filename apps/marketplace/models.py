import uuid
from django.db import models
from django.conf import settings

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # ALPHANUMERIC ID
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    edition = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Listing(models.Model):
    LISTING_TYPES = (('SELL', 'Sell'), ('TRADE', 'Trade'))
    CONDITIONS = (('NEW', 'New'), ('LIKE_NEW', 'Like New'), ('GOOD', 'Good'), ('ACCEPTABLE', 'Acceptable'))
    STATUS = (('ACTIVE', 'Active'), ('SOLD', 'Sold/Traded'), ('CLOSED', 'Closed'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # ALPHANUMERIC ID
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='listings')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    asking_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    condition = models.CharField(max_length=15, choices=CONDITIONS)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='ACTIVE')
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.condition}"