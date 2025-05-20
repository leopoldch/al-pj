from django.urls import path, include
from .views import MessageView, ProfileView, BucketPointView

urlpatterns = [
    path("messages/", MessageView.as_view(), name="user_messages"),
    path("messages/<int:pk>/", MessageView.as_view(), name="user_messages"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
    path("bucketpoints/", BucketPointView.as_view(), name="bucket_points"),
    path("bucketpoints/<int:pk>/", BucketPointView.as_view(), name="bucket_points"),
]
