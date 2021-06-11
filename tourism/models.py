from django.db import models


class AdminModel(models.Model):
    idno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contact = models.IntegerField(unique=True)
    email = models.EmailField(max_length=100,unique=True)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)


class CustomerModel(models.Model):
    cno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='customer_images/')


class PackageModel(models.Model):
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=200,unique=True)
    pduration = models.CharField(max_length=10)
    pdescription = models.CharField(max_length=300)
    prating = models.FloatField(max_length=10)
    price = models.IntegerField()
    image = models.ImageField(upload_to='package_images/', default=False)


class EnquiryModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.IntegerField(unique=True)
    date_of_travel = models.DateField()
    no_of_people = models.IntegerField()
    message = models.CharField(max_length=300)


class PackDetailsModel(models.Model):
    pckid = models.AutoField(primary_key=True)
    tid = models.IntegerField()
    pid = models.OneToOneField(PackageModel,on_delete=models.CASCADE)