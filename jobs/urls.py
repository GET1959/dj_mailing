from django.urls import path

from jobs.apps import JobsConfig
from jobs.views import (
    MailingCreateView,
    MailingListView,
    MailingDetailView,
    MailingUpdateView,
    MailingDeleteView,
    AttemptListView, activity_trigger, HomeView,
)

app_name = JobsConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("create/", MailingCreateView.as_view(), name="create"),
    path("list/", MailingListView.as_view(), name="list"),
    path("view/<int:pk>/", MailingDetailView.as_view(), name="view"),
    path("edit/<int:pk>/", MailingUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", MailingDeleteView.as_view(), name="delete"),
    path('activity/<int:pk>/', activity_trigger, name='activity_trigger'),
    path("attempts", AttemptListView.as_view(), name="attempt_list"),
]
