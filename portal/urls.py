from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^registration$', views.register, name='register'),
url(r'^loggedin$', views.login_page, name='loggedin'),
url(r'^librarian$', views.librarian, name='librarian'),
url(r'^customer$', views.customer, name='customer')
]
