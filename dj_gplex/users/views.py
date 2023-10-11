from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import CustomUserCreationForm


def dashboard(request):
    return render(request, "users/dashboard.html")
