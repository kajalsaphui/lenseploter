from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200, null=True)
    application_name = models.CharField(max_length=200, null=True)
    castomer_code = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r"^\+(?:[0-9]●?){6,14}[0-9]$", message=_("Enter a valid international mobile phone number starting with +(country code)"))
    mobile_phone = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17, blank=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.application_name}: {self.country}:{self.castomer_code}"

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Excilent', 'Excilent'),
			('Outstanding', 'Outstanding'),
            ('Standard', 'Standard'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return f"{self.name}: {self.date_created}: {self.price}"

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return f"{self.product}:{self.customer}: {self.date_created}: {self.status}"

class master(models.Model):
    Cust_code = models.CharField(max_length=200, null=True)
    Ref_cust_code = models.CharField(max_length=200, null=True)
    Table_name = models.CharField(max_length=200, null=True)
    ApplicationName = models.CharField(max_length=200, null=True)
    status = models.BooleanField(null=True, default=1)

    def __str__(self):
        return f"{self.Cust_code}:{self.Table_name}: {self.ApplicationName}: {self.status}"