from django.shortcuts import render, redirect, reverse
from django.http import Http404
from accounts.forms import SearchForm, UserInfoForm
from accounts.models import User
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


# Create your views here.

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        users = User.objects.search(**form.cleaned_data)
    else:
        users = User.objects.all()
        form = SearchForm()
    return render(request, "account/search.html", {"form": form, "users": users})

def profile(request, username=None):
    if request.user.is_authenticated==False and username==None:
        return redirect(reverse('index'))
    if username==None:
        return redirect(reverse('profile_info'))
    else:
        try:
            user=User.objects.get(username=username)
        except:
            raise Http404()
    return render(request,"account/profile.html", {"user":user})

def index(request):
    return render(request, 'account/index.html')

@login_required
def user_info(request):
    user = request.user
    if request.method == "POST":
        #apply changes
        form=SearchForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name =form['first_name']
            user.last_name =form['last_name']
            user.full_name = (form['first_name']+" "+form['last_name'])
            user.country = form['country']
            user.skills = form['skills']
            user.bio = form['bio']
            user.linked_in_link = form['linked_in_link']
            user.crypto_public_key = form['crypto_public_key']
            user.paypal_email = form['paypal_email']
            if form['profile_picture'] != None:
                user.profile_picture = form['profile_picture']
            if user.username is None:
                try: 
                    username = SocialAccount.objects.get(user=request.user).extra_data['login']
                    user.username=username
                except ObjectDoesNotExist:
                    raise Http404()
            try:
                user.save()
            except IntegrityError:
                raise Http404()
            return redirect(user.get_absolute_url())
    if user.username == None:
        form = UserInfoForm()
    else:
        initial_values = {
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'country': user.country, 
            'profile_picture': user.profile_picture,
            'skills': user.skills,
            'bio': user.bio,
            'paypal_email': user.paypal_email,
            'crypto_public_key': user.crypto_public_key,
            'linked_in_link': user.linked_in_link,
            }
        form=UserInfoForm(initial=initial_values)
    return render(request, 'account/profile_info.html', {"form": form})

