from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime
from django.db import connection


user = ''			# Global variable for user

def index(request):
	return render(request, 'portal/index.html')


def register(request):
	postobjects = request.POST.copy()
	firstnamelib=postobjects.get('firstnamelib')
	lastnamelib=postobjects.get('lastnamelib')
	passwordlib=postobjects.get('passwordlib')
	firstnamecust=postobjects.get('firstnamecust')
	lastnamecust=postobjects.get('lastnamecust')
	passwordcust=postobjects.get('passwordcust')
	reg_date=datetime.now()
	cursor = connection.cursor()
	
	if firstnamecust == None:	# Librarian case
		newentry = login_librarian.objects.create(firstname=firstnamelib,lastname=lastnamelib,password=passwordlib, reg_date=reg_date)
		tablename =  "LIBRARIAN" + passwordlib 
		# cursor.execute("create table %s(id integer AUTO_INCREMENT NOT NULL PRIMARY KEY, book_name varchar(30) NOT NULL, reg_date date)" %(tablename))
		
	else:						# Customer Case
		newentry = login_customer.objects.create(firstname=firstnamecust,lastname=lastnamecust,password=passwordcust, reg_date=reg_date)
		tablename = "CUSTOMER" + passwordcust
		cursor.execute("create table %s(id integer AUTO_INCREMENT NOT NULL PRIMARY KEY, book_name varchar(30) NOT NULL, request_date date, issue_status varchar(10) DEFAULT 'Pending')" %(tablename))
	
	cursor.close()
	
	return render(request, 'portal/index.html')
	# return HttpResponseRedirect(reverse('portal:login_page'))



def login_page(request):
	global user
	postobjects = request.POST.copy()
	firstnamelib=postobjects.get('firstnamelib')
	passwordlib=postobjects.get('passwordlib')
	firstnamecust=postobjects.get('firstnamecust')
	passwordcust=postobjects.get('passwordcust')
	
	if firstnamecust == None:		# Librarian case
		tablename =   "LIBRARIAN" + passwordlib
		c = login_librarian.objects.filter(firstname=firstnamelib, password=passwordlib).count()
		if c == 0:				# Not a registered user
			return render(request, 'portal/registration.html')
		else:
			user = tablename
			return render(request, 'portal/librarian.html')
	
	else:							# Customer Case
		tablename = "CUSTOMER" + passwordcust
		c = login_customer.objects.filter(firstname=firstnamecust, password=passwordcust).count() 
		if c == 0:			# Not a registered user
			return render(request, 'portal/registration.html')
		else:
			user = tablename
			return render(request, 'portal/customer.html')



def librarian(request):
	postobjects = request.POST.copy()
	addbook=postobjects.get('addbook')
	addsect=postobjects.get('addsect')
	old_name=postobjects.get('old_name')
	new_name=postobjects.get('new_name')
	delbook=postobjects.get('delbook')

	if delbook == None and old_name == None and addbook != None: 		# adding Case
		newentry = books.objects.create(bookname=addbook,section=addsect)
	
	elif addbook == None and delbook == None and old_name != None:		# editing Case
		c = books.objects.filter(bookname=old_name).count() 
		if c != 0:
			cursor = connection.cursor()
			cursor.execute("update portal_books set bookname = %s where bookname = %s;" % (str(new_name), str(old_name)))
			cursor.close()

	else:				# delete case
		c = books.objects.filter(bookname=delbook).count()
		if c != 0:
			cursor = connection.cursor()
			cursor.execute("delete from portal_books where bookname = %s;" % (str(delbook)))
			cursor.close()
	
	return render(request, 'portal/librarian.html')			# Retuns the same page back



def customer(request):
	global user
	postobjects = request.POST.copy()
	book_name=postobjects.get('book_name')
	book_issued=postobjects.get('book_issued')
	sortbook = postobjects.get('sortbook')
	request_date = datetime.now()
	cursor = connection.cursor()
	lt = cursor.execute("Select issue_status from %s" % (user))		# user is the table name
	cursor.close()

	if book_issued == None and book_name != None and sortbook == None:		# Request case
		c = books.objects.filter(bookname=book_name).count() 
		if c != 0:				# Issue only one book to user
			curs = connection.cursor()
			curs.execute("Insert into %s VALUES (bookname=%s, request_date=%s, issue_status = %s);" %(user, book_name, request_date, 'Pending'))
			curs.close()

	elif book_issued != None and book_name == None and sortbook == None:						# Return Case
		curs = connection.cursor()
		curs.execute("delete from %s where bookname = %s;" % (user, str(book_issued)))
		curs.close()

	elif sortbook != None and book_name == None and book_issued == None:		# Sort Case
		curs = connection.cursor()
		output = curs.execute("select * from %s where section = %s order by bookname;" % ('portal_books', str(sortbook)))
		curs.close()
		return HttpResponse(output)

	return render(request, "portal/customer.html")

# Create your views here.
