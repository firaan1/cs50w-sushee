from shopping.models import *
import csv, subprocess, os
from django.core.files import File


print("Importing Color from prep/html_common_colors.csv")
if Color.objects.count() > 0:
    print("Skipping...")
else:
    # importing colors
    f = open("prep/html_common_colors.csv")
    reader = csv.reader(f)
    for name, code in reader:
        print(f"{name}")
        c = Color(name = name, code = code)
        c.save()
        del(c)

print("Importing KurtaSize from prep/kurtasize.csv")
if KurtaSize.objects.count() > 0:
    print("Skipping...")
else:
    # importing kurtasize
    f = open("prep/kurtasize.csv")
    reader = csv.reader(f)
    for size, tofitbust, frontlength, tofitwaist, tofithip in reader:
        print(f"{size}")
        c = KurtaSize(size = size, tofitbust = tofitbust, frontlength = frontlength, tofitwaist = tofitwaist, tofithip = tofithip)
        c.save()
        del(c)


print("Importing TopSize from prep/topsize.csv")
if TopSize.objects.count() > 0:
    print("Skipping...")
else:
    # importing colors
    f = open("prep/topsize.csv")
    reader = csv.reader(f)
    for size, tofitbust, frontlength, tofitwaist in reader:
        print(f"{size}")
        c = TopSize(size = size, tofitbust = tofitbust, frontlength = frontlength, tofitwaist = tofitwaist)
        c.save()
        del(c)

print("Importing TrouserSize from prep/trousersize.csv")
if TrouserSize.objects.count() > 0:
    print("Skipping...")
else:
    # importing colors
    f = open("prep/trousersize.csv")
    reader = csv.reader(f)
    for size, tofitwaist, tofithip in reader:
        print(f"{size}")
        c = TrouserSize(size = size, tofitwaist = tofitwaist, tofithip = tofithip)
        c.save()
        del(c)

print("Importing SareeSize")
if SareeSize.objects.count() > 0:
    print("Skipping...")
else:
    # for sarees
    s = SareeSize()
    s.save()
    del(s)

#

#
print("Adding data to tables from prep/dresses/.")
print("Adding KurtaRate")
if KurtaRate.objects.count() > 0:
    print("Skipping...")
else:
    dir = "prep/dresses/kurta"
    dtype = {"Angrakha Kurti" : 1000, "Cotton Kurti" : 1500, "Two Face Kurti" : 1200}
    p = subprocess.Popen(['ls', dir], stdout = subprocess.PIPE)
    filelist = p.communicate()
    filelist = filelist[0].decode('utf-8').split('\n')
    for f in filelist:
        if f == "":
            continue
        print(f"{f}")
        name, model, color, size = f.split("_")
        size1 = size.split(".")[:-1]
        size = []
        for s in size1:
            size.append(KurtaSize.objects.get(size = s))
        ufile = File(open(os.path.join(dir, f), 'rb'))
        uploads = []
        upload = Document(document = ufile, filename = f, color = Color.objects.get(name = color.upper()))
        upload.save()
        uploads.append(upload)
        dress = KurtaRate(name = name, model = model, price = dtype[model])
        dress.save()
        dress.size.set(size)
        dress.save()
        dress.image.set(uploads)
        dress.save()

print("Adding SareeRate")
if SareeRate.objects.count() > 0:
    print("Skipping...")
else:
    dir = "prep/dresses/saree"
    dtype = {"Bomkai" : 1800, "Chanderi" : 2000, "Kanjeevaram" : 5000, "Konrad" : 1200, "Mysore Saree" : 1750, "Paithani" : 1050}
    p = subprocess.Popen(['ls', dir], stdout = subprocess.PIPE)
    filelist = p.communicate()
    filelist = filelist[0].decode('utf-8').split('\n')
    for f in filelist:
        if f == "":
            continue
        print(f"{f}")
        name, model, color = f.split("_")
        color = color.split(".")[:-1][0]
        size = [SareeSize.objects.first()]
        ufile = File(open(os.path.join(dir, f), 'rb'))
        uploads = []
        upload = Document(document = ufile, filename = f, color = Color.objects.get(name = color.upper()))
        upload.save()
        uploads.append(upload)
        dress = SareeRate(name = name, model = model, price = dtype[model])
        dress.save()
        dress.size.set(size)
        dress.save()
        dress.image.set(uploads)
        dress.save()
    dir = "prep/dresses/saree2"
    dtype = {"GoldenYarn" : 2000 }
    p = subprocess.Popen(['ls', dir], stdout = subprocess.PIPE)
    filelist = p.communicate()
    filelist = filelist[0].decode('utf-8').split('\n')
    uploads = []
    for f in filelist:
        if f == "":
            continue
        print(f"{f}")
        name, model, color = f.split("_")
        color = color.split(".")[:-1][0]
        size = [SareeSize.objects.first()]
        ufile = File(open(os.path.join(dir, f), 'rb'))
        upload = Document(document = ufile, filename = f, color = Color.objects.get(name = color.upper()))
        upload.save()
        uploads.append(upload)
    dress = SareeRate(name = name, model = model, price = dtype[model])
    dress.save()
    dress.size.set(size)
    dress.save()
    dress.image.set(uploads)
    dress.save()

print("Adding TopRate")
if TopRate.objects.count() > 0:
    print("Skipping...")
else:
    dir = "prep/dresses/top"
    dtype = {"Asymmetric Top" : 400, "Lace Top" : 320, "Regular" : 300, "Shirt Top" : 450, "Tunic Top" : 500}
    p = subprocess.Popen(['ls', dir], stdout = subprocess.PIPE)
    filelist = p.communicate()
    filelist = filelist[0].decode('utf-8').split('\n')
    for f in filelist:
        if f == "":
            continue
        print(f"{f}")
        name, model, color, size = f.split("_")
        size1 = size.split(".")[:-1]
        size = []
        for s in size1:
            size.append(TopSize.objects.get(size = s))
        ufile = File(open(os.path.join(dir, f), 'rb'))
        uploads = []
        upload = Document(document = ufile, filename = f, color = Color.objects.get(name = color.upper()))
        upload.save()
        uploads.append(upload)
        dress = TopRate(name = name, model = model, price = dtype[model])
        dress.save()
        dress.size.set(size)
        dress.save()
        dress.image.set(uploads)
        dress.save()

print("Adding TrouserRate")
if TrouserRate.objects.count() > 0:
    print("Skipping...")
else:
    dir = "prep/dresses/trouser"
    dtype = {"Casual" : 300, "Slim Fit" : 320}
    p = subprocess.Popen(['ls', dir], stdout = subprocess.PIPE)
    filelist = p.communicate()
    filelist = filelist[0].decode('utf-8').split('\n')
    for f in filelist:
        if f == "":
            continue
        print(f"{f}")
        name, model, color, size = f.split("_")
        size1 = size.split(".")[:-1]
        size = []
        for s in size1:
            size.append(TrouserSize.objects.get(size = s))
        ufile = File(open(os.path.join(dir, f), 'rb'))
        uploads = []
        upload = Document(document = ufile, filename = f, color = Color.objects.get(name = color.upper()))
        upload.save()
        uploads.append(upload)
        dress = TrouserRate(name = name, model = model, price = dtype[model])
        dress.save()
        dress.size.set(size)
        dress.save()
        dress.image.set(uploads)
        dress.save()
