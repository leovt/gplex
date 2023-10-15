from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.signing import TimestampSigner
from django.http import JsonResponse

from .models import Profile

def create_token(request):
    signer = TimestampSigner()
    return signer.sign(request.user.username)

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except:
        profile = Profile(user=request.user)
        profile.save()

    return render(request, "users/dashboard.html", {
        'profile': profile,
        'ws_auth_token': create_token(request),
    })

@login_required
def wstoken(request):
    return JsonResponse({
        "ws_auth_token": create_token(request),
    })
