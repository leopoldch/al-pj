from django.urls import path
from .views import MessageView, ProfileView

urlpatterns = [
    path("messages/", MessageView.as_view(), name="user_messages"),
    path("messages/<int:pk>/", MessageView.as_view(), name="user_messages"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
]
