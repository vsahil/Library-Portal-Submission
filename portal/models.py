from django.db import models
from django.utils import timezone
import datetime

class login_librarian(models.Model):
	"""docstring for login"""
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	reg_date = models.DateTimeField('date published')
	# def __str__(self):
		# return self.firstname

class login_customer(models.Model):
	"""docstring for login"""
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	reg_date = models.DateTimeField('date published')

class books(models.Model):
	"""docstring for books"""
	bookname = models.CharField(max_length=200)
	section = models.CharField(max_length=200)

		
# Create your models here.
