from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import Profile
from fundraising.models import Project
from django.utils import timezone
from notifications.models import Notification
from notifications.signals import notify

now = timezone.now()

# view for the registration of a new user
def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user)
            login(request, user)
            notify.send(
                request.user,
                recipient=request.user,
                verb=f"Welcome to STICK TO GET THERE {user.username}!",
                timestamp=now,
            )
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/registration.html", context)


# collecting user favourite projects
def favourites_view(request):

    profile = Profile.objects.get(user=request.user)
    favourites = profile.favourites.all()

    context = {
        "profile": profile,
        "favourites": favourites,
    }

    return render(request, "accounts/favourites.html", context)
