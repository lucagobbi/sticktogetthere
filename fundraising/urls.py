from os import name
from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.home_view, name="homepage"),
    path("about/", v.about_view, name="about"),
    path("search/", v.search_view, name="search"),
    path("notifications/", v.notifications_view, name="view_all"),
    path("notifications/delete/", v.notifications_delete_view, name="delete"),
    path("projects/", v.projects_view, name="projects"),
    path("projects/<int:id>/", v.project_detail_view, name="project-detail"),
    path(
        "projects/<int:id>/favourite/",
        v.add_remove_favourite_view,
        name="add-remove-favourite",
    ),
    path("projects/<int:id>/contribute/", v.contribute_view, name="contribute"),
    path(
        "projects/<int:id>/requests/", v.project_requests_view, name="project-requests"
    ),
    path("requests/<int:id>/", v.request_detail_view, name="request-detail"),
    path("requests/<int:id>/vote/", v.vote_view, name="vote"),
    path("requests/<int:id>/send-payment/", v.send_payment_view, name="send-payment"),
    path("projects/<int:id>/newrequest/", v.new_request_view, name="newrequest"),
    path("newproject/", v.new_project_view, name="newproject"),
]
