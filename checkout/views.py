from django.shortcuts import render, redirect

# Create your views here.


def checkout(request):
    """view to return the stripe checkout page"""
    print("Check it out")

    return redirect("home:main-menu")
