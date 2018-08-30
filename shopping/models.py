from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

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
# class KurtaRate(models.Model):
#     name = models.CharField(max_length = 100)
#     model = models.CharField(max_length = 25)
#     size = models.ForeignKey(KurtaSize, on_delete = models.CASCADE, related_name = "kurta_size")
#     colour = models.ForeignKey(Colour, on_delete = models.SET_NULL, null = True, related_name = "kurta_colour")
