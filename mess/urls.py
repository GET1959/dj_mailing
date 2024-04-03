from django.urls import path

from mess.apps import MessConfig
from mess.views import MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView

app_name = MessConfig.name

urlpatterns = [
    path('create/', MessageCreateView.as_view(), name='create'),
    path('', MessageListView.as_view(), name='list'),
    path('view/<int:pk>/', MessageDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', MessageUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='delete'),
]