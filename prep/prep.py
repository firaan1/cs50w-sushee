from shopping.models import *
import csv

# importing colours
f = open("prep/html_colours.csv")
reader = csv.reader(f)
for name, code in reader:
    name
    c = Colour(name = name, code = code)
    c.save()
    del(c)

# importing kurtasize
f = open("prep/kurtasize.csv")
reader = csv.reader(f)
for size, tofitbust, frontlength, tofitwaist, tofithip in reader:
    size
    c = KurtaSize(size = size, tofitbust = tofitbust, frontlength = frontlength, tofitwaist = tofitwaist, tofithip = tofithip)
    c.save()
    del(c)

# importing colours
f = open("prep/topsize.csv")
reader = csv.reader(f)
for size, tofitbust, frontlength, tofitwaist in reader:
    size
    c = TopSize(size = size, tofitbust = tofitbust, frontlength = frontlength, tofitwaist = tofitwaist)
    c.save()
    del(c)

# importing colours
f = open("prep/trousersize.csv")
reader = csv.reader(f)
for size, tofitwaist, tofithip in reader:
    size
    c = TrouserSize(size = size, tofitwaist = tofitwaist, tofithip = tofithip)
    c.save()
    del(c)