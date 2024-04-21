from django.urls import path

from jobs.apps import JobsConfig
from jobs.views import (
    MailingCreateView,
    MailingListView,
    MailingDetailView,
    MailingUpdateView,
    MailingDeleteView,
    AttemptListView,
)

app_name = JobsConfig.name

urlpatterns = [
    path("create/", MailingCreateView.as_view(), name="create"),
    path("", MailingListView.as_view(), name="list"),
    path("view/<int:pk>/", MailingDetailView.as_view(), name="view"),
    path("edit/<int:pk>/", MailingUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", MailingDeleteView.as_view(), name="delete"),
    path("attempts", AttemptListView.as_view(), name="attempt_list"),
]
