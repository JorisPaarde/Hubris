from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from profiles.models import Profile


# Create your views here.


def checkout(request):
    """view to return the stripe checkout page"""
    current_user = request.user
    print("Check it out")
    payed_full_version = current_user.profile.payed_full_version
    user_email = current_user.email
    bio = current_user.profile.bio
    print(payed_full_version)
    print(user_email)
    print(bio)

    return redirect("home:main-menu")
