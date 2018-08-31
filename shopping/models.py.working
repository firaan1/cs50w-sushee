from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    datetime = models.DateTimeField(auto_now_add=True)

# rates
class KurtaRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="kurta", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "kurta_image")
    size = models.ForeignKey(KurtaSize, on_delete = models.CASCADE, related_name = "kurta_size")
    size = models.ManyToManyField(KurtaSize, related_name = "kurta_size")
    color = models.ForeignKey(Color, on_delete = models.SET_NULL, null = True, related_name = "kurta_color")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"

class TopRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="top", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "top_image")
    size = models.ForeignKey(TopSize, on_delete = models.CASCADE, related_name = "top_size")
    color = models.ForeignKey(Color, on_delete = models.SET_NULL, null = True, related_name = "top_color")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"

class TrouserRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="trouser", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "trouser_image")
    size = models.ForeignKey(TrouserSize, on_delete = models.CASCADE, related_name = "trouser_size")
    color = models.ForeignKey(Color, on_delete = models.SET_NULL, null = True, related_name = "trouser_color")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"

class SareeRate(models.Model):
    dresstype = models.CharField(max_length = 25, default="saree", editable = False)
    name = models.CharField(max_length = 100)
    model = models.CharField(max_length = 25)
    image = models.ManyToManyField(Document, related_name = "saree_image")
    size = models.ForeignKey(SareeSize, on_delete = models.CASCADE, related_name = "saree_size")
    color = models.ForeignKey(Color, on_delete = models.SET_NULL, null = True, related_name = "saree_color")
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    def __str__(self):
        return f"{self.name} cost {rupees}{self.price}"
