# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'books_app/index.html')

def register(request):
	if request.method == "POST":
		errors = Users.objects.validate(request.POST)
		if errors:
			for tags, error in errors.iteritems():
				messages.error(request, error, extra_tags=tags)
		else:
			hashed_pass = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt())
			user = Users.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pass)
			request.session['user_id'] = user.id
			request.session['user_alias'] = user.alias
			return redirect('/books')
	return redirect('/')

def logout(request):
	request.session['user_id'] = 0
	return redirect('/')

def login(request):
	if request.method == "POST":
		email = request.POST['email']
		user = Users.objects.get(email = email)
		if bcrypt.checkpw(request.POST['pass'].encode(), user.password.encode()):
			request.session['user_id'] = user.id
			request.session['user_alias'] = user.alias
			return redirect('/books')
	return redirect('/')

def home(request):
	if request.session['user_id'] == 0:
		messages.error(request, "Not logged in")
		return redirect('/')
	else:
		context = {
		'books': Books.objects.all().values(),
		'recent_reviews': Reviews.objects.all().order_by('-id')[:3]
		}
		return render(request, 'books_app/book_home.html', context)

def addbook(request):
	context = {
	"books": Books.objects.all()
	}
	return render(request, 'books_app/add_book.html', context)

def createbook(request):
	if request.method == "POST": 
		book = Books.objects.create(title = request.POST['title'], author =request.POST['author'])
		
		user = Users.objects.get(id = request.session['user_id'])
		review = Reviews.objects.create(book = book, user = user, text = request.POST['review'], rating = request.POST['rating'])
	return redirect('/books')

def viewbook(request, id):
	context = {
	'book': Books.objects.get(id = id),
	'reviews': Reviews.objects.all().filter(book__id = id)
	}
	return render(request, 'books_app/book_info.html', context)

def addreview(request, id):
	if request.method == "POST":
		user_id = request.session['user_id']
		book = Books.objects.get(id = id)
		user = Users.objects.get(id = user_id)
		Reviews.objects.create(book = book, user = user, text = request.POST['text'], rating = request.POST['rating'])
	return redirect('/books/' + id)

def viewuser(request, id):
	context = {
	'user': Users.objects.get(id = id),
	'reviews_count': len(Reviews.objects.filter(user__id = id)),
	'reviews': Reviews.objects.filter(user__id = id)
	}
	return render(request, 'books_app/user_info.html', context)