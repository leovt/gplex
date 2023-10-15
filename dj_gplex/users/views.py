from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.signing import TimestampSigner
from django.http import JsonResponse

from .models import Profile

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except:
        profile = Profile(user=request.user)
        profile.save()

    return render(request, "users/dashboard.html", {
        'profile': profile,
    })

@login_required
def wstoken(request):
    signer = TimestampSigner()
    token = signer.sign(request.user.username)
    return JsonResponse({"token": token})
