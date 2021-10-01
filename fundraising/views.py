from logging import log
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from notifications.models import Notification
from toolz.itertoolz import get
from .models import Project, Request
from .forms import ProjectForm, RequestForm
from notifications.signals import notify
from .utils import *


now = timezone.now()
notifications = Notification.objects.all()


@login_required
def home_view(request):

    projects = Project.objects.all().order_by("-date_created")

    context = {
        "projects": projects[:3],
        "notifications": notifications,
    }

    return render(request, "fundraising/homepage.html", context)


# list of all projects
@login_required
def projects_view(request):

    projects = Project.objects.all()

    context = {
        "projects": projects,
    }

    return render(request, "fundraising/projects.html", context)


# single page project
@login_required
def project_detail_view(request, id):

    project = get_object_or_404(Project, id=id)
    balance = getBalance(project.address)
    numberOfContributors = getNumberOfContributors(project.address)
    profile = Profile.objects.get(user=request.user)

    context = {
        "project": project,
        "balance": balance,
        "numberOfContributors": numberOfContributors,
        "profile": profile,
    }

    return render(request, "fundraising/project_detail.html", context)


# view to add or remove projects from favourites not rendering a template
@login_required
def add_remove_favourite_view(request, id):

    user = request.user
    project = get_object_or_404(Project, id=id)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":

        if project in profile.favourites.all():
            profile.favourites.remove(project)
        else:
            profile.favourites.add(project)

    profile.save()

    return redirect(f"/projects/{ project.id }/")


# contribute page - actions are built in the front end with web3.js
@login_required
def contribute_view(request, id):
    project = get_object_or_404(Project, id=id)
    contractAddress = web3.toChecksumAddress(project.address)

    context = {"project": project, "contractAddress": contractAddress}

    return render(request, "fundraising/contribute.html", context)


# all requests for a single project
@login_required
def project_requests_view(request, id):
    project = get_object_or_404(Project, id=id)
    open_requests = Request.objects.filter(project=project, completed=False)
    done_requests = Request.objects.filter(project=project, completed=True)

    context = {
        "project": project,
        "open_requests": open_requests,
        "done_requests": done_requests,
    }

    return render(request, "fundraising/project_requests.html", context)


# single request page
@login_required
def request_detail_view(request, id):

    req = get_object_or_404(Request, id=id)

    address = req.project.address
    requestNo = req.getRequestNo()

    numberOfVoters = getNumberOfVoters(address, requestNo)

    numberOfContributors = getNumberOfContributors(address)

    # calculating consensus for this request
    if numberOfContributors == 0:
        consensus = 0
    else:
        consensus = float((numberOfVoters / numberOfContributors)) * 100

    requestNo = req.getRequestNo()

    context = {
        "request": req,
        "numberOfVoters": numberOfVoters,
        "requestNo": requestNo,
        "consensus": consensus,
    }

    return render(request, "fundraising/request_detail.html", context)


# vote page - actions are built in the front end with web3.js
@login_required
def vote_view(request, id):

    req = get_object_or_404(Request, id=id)

    requestNo = req.getRequestNo()

    context = {
        "request": req,
        "requestNo": requestNo,
    }

    return render(request, "fundraising/vote.html", context)


# page for completing a request - action from the back end since only admin can call this function
@staff_member_required
def send_payment_view(request, id):

    req = get_object_or_404(Request, id=id)
    req.sendPayment()
    req.completed = True
    req.save()

    req_title = (str(req.description))[0:20]

    notify.send(
        request.user,
        recipient=request.user,
        verb=f"{req_title} - request finalized!",
        timestamp=now,
    )

    return redirect("/")


# form view to create a new project - only administrators can create new projects
@staff_member_required
def new_project_view(request):

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            form.instance.admin = request.user

            # check some conditions
            if form.instance.goal < 0:
                messages.warning(request, "You cannot open a project without a goal!")
                return redirect("/newproject/")
            if form.instance.deadline < now:
                messages.warning(request, "You cannot set a deadline already reached!")
                return redirect("/newproject/")

            # if all conditions are met deploy the contract
            form.instance.deploy_contract()
            form.save()

            notify.send(
                request.user,
                recipient=request.user,
                verb=f"Project - {form.instance.title} - is opened!",
                timestamp=now,
            )
            return redirect("/")

    else:
        form = ProjectForm()

    context = {
        "form": form,
        "notifications": notifications,
    }

    return render(request, "fundraising/newproject.html", context)


# form view to create a new request - only administrators can propose a request
@staff_member_required
def new_request_view(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == "POST":
        form = RequestForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.instance.project = project

            if form.instance.value < 0:
                messages.warning(
                    request, "You have to set a positive value for this field!"
                )
                return redirect("/newrequest/")

        # call the contract for this specific project and create a request
        form.instance.createRequest(
            form.instance.description, form.instance.addressTo, int(form.instance.value)
        )
        form.save()

        notify.send(
            request.user,
            recipient=request.user,
            verb=f"Request opened for {project.title}",
            timestamp=now,
        )
        return redirect(f"/projects/{id}/requests")

    else:
        form = RequestForm()

    context = {
        "form": form,
        "notifications": notifications,
    }

    return render(request, "fundraising/newrequest.html", context)


# about page
@login_required
def about_view(request):
    return render(request, "fundraising/about.html")


# search function
@login_required
def search_view(request):

    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect("/search/")
        projects = Project.objects.filter(title__icontains=querystring)
        context = {
            "projects": projects,
            "querystring": querystring,
            "notifications": notifications,
        }
        return render(request, "fundraising/search.html", context)

    else:
        return render(request, "fundraising/search.html")


# notifications view - view all notification and update read parameter
@staff_member_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by(
        "-timestamp"
    )

    notifications.mark_all_as_read()
    notifications.update()

    context = {"notifications": notifications}

    return render(request, "fundraising/notifications.html", context)


# view for deleting all notifications
@staff_member_required
def notifications_delete_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications.delete()
    return redirect("/notifications/")
