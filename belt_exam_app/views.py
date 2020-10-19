from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    # Check if post request
    if request.method == "POST":
        # check if register object is valid
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value,extra_tags=key)
            return redirect('/')
        # check to see if user email is already in use
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request,"Email is already in use")
            return redirect ('/')
        # Hash the password with Bcrypt
        pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        # Now that you've hashed pw, you can create user in database
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw
        )
        # Now you can put user_id into session
        request.session['user_id'] = User.objects.last().id
        return redirect('/dashboard')
    else:
        return redirect('/')

def login(request):
    # check if POST REQUEST
    if request.method == "POST":
        # validate the login object
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        # check to see if email is in database
        user = User.objects.filter(email=request.POST['login_email'])
        if not user:
            messages.error(request,"Invalid Email/Password")
            return redirect ('/')
        # check if passwords match
        if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
            messages.error(request,"Invalid Email/Password")
            return redirect ('/')
        # put user_id into session and redirect
        request.session['user_id'] = user[0].id
        return redirect ('/dashboard')
    else:
        return redirect ('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_authors' : Author.objects.all()
        }
        return render(request, 'dashboard.html', context)

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect ('/')

def add_author(request):
    if request.method == "POST":
        errors = Author.objects.author_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect ('/dashboard')

        Author.objects.create(
            author = request.POST['author'],
            quote = request.POST['quote'],
            user = User.objects.get(id=request.session['user_id'])
        )
        return redirect('/dashboard')
    else:
        return redirect('/logout')

def destroy_author(request, author_id):
    destroy_author = Author.objects.get(id=author_id)
    destroy_author.delete()
    return redirect ('/dashboard')

def edit_user(request):
    context = {
        'edit' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "edit_user.html", context)

def update_user(request):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect ('/edit_user')
        update = User.objects.get(id=request.session['user_id'])
        update.first_name = request.POST['edit_first_name']
        update.last_name = request.POST['edit_last_name']
        update.email = request.POST['edit_email']
        update.save()
        return redirect('/dashboard')
    else:
        return redirect ('/logout')

def user_quotes(request, user_id):
    context = {
        'user' : User.objects.get(id=user_id)
    }
    return render(request, "user_quotes.html", context)

def like(request, author_id, user_id):
    author = Author.objects.get(id=author_id)
    user = User.objects.get(id=user_id)

    author.likes.add(user)
    return redirect('/dashboard')
