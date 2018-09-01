from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from model_utils import Choices
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

# Create your models here.
# indian rupees
rupees = u"\u20B9"

## size chart
# Indian & fusion wear
# kurtas
class KurtaSize(models.Model):
    size = models.CharField(max_length = 4, unique = True)
    tofitbust = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    frontlength = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    tofitwaist = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    tofithip = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    def __str__(self):
        return f"{self.size}"

# tops
class TopSize(models.Model):
    size = models.CharField(max_length = 4, unique = True)
    tofitbust = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    frontlength = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    tofitwaist = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    def __str__(self):
        return f"{self.size}"

# trousers
class TrouserSize(models.Model):
    size = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], unique = True)
    tofitwaist = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    tofithip = models.DecimalField(max_digits = 5, decimal_places = 1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    def __str__(self):
        return f"{self.size}"

class SareeSize(models.Model):
    size = models.CharField(max_length = 25, default="Free Size", unique = True)
    def __str__(self):
        return f"{self.size}"

# saree & blouses (free size)

## colors
class Color(models.Model):
    name = models.CharField(max_length = 25, unique = True)
    code = models.CharField(max_length = 7)
    def __str__(self):
        return f"{self.name}"

# image upload
class Document(models.Model):
    document = models.FileField(upload_to='documents/%Y/%m/%d')
    color = models.ForeignKey(Color, on_delete = models.SET_NULL, null = True, related_name = "dress_color")
    datetime = models.DateTimeField(auto_now_add=True)

# rates
class KurtaRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="kurta", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "kurta_image")
    size = models.ManyToManyField(KurtaSize, related_name = "kurta_size")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"

class TopRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="top", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "top_image")
    size = models.ManyToManyField(TopSize, related_name = "top_size")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"

class TrouserRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="trouser", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "trouser_image")
    size = models.ManyToManyField(TrouserSize, related_name = "trouser_size")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"

class SareeRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="saree", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "saree_image")
    size = models.ManyToManyField(SareeSize, related_name = "saree_size")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"

class DressOrder(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = "dress_user")
    dresstype = models.CharField(max_length = 25)
    dresspk = models.IntegerField()
    sizepk = models.IntegerField()
    paid = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.dresstype}"

class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = "address_user")
    address = models.CharField(max_length = 1000)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    # taken from https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    def __str__(self):
        return f"{self.address}, {self.phone_number}"

class PlacedOrder(models.Model):
    STATUS = Choices(
        ('new', _('new')),
        ('in_progress', _('in_progress')),
        ('delivered', _('delivered'))
    )
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = "ordered_user")
    deliveryaddress = models.ForeignKey(DeliveryAddress, on_delete = models.SET_NULL, null = True, related_name = "delivery_address")
    order = models.ManyToManyField(DressOrder, related_name = "ordered_dress")
    status = models.CharField(choices = STATUS, default = STATUS.new, max_length = 25)
    datetime = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits = 9, decimal_places = 2)
    def __str__(self):
        return f"status: {self.status}; total: {self.total}"

class UserInput(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = "input_user")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null = True)
    review = models.CharField(max_length = 1000, null = True)
    dresspk = models.IntegerField()
    class Meta:
        unique_together = ["user", "dresspk"]
    def __str__(self):
        return f"{self.rating}"
