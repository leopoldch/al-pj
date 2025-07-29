from django.urls import path
from .views import (
    MessageView,
    ProfileView,
    BucketPointView,
    PresenceIndicatorView,
    AlbumView,
    PhotoView,
)

urlpatterns = [
    path("messages/", MessageView.as_view(), name="user_messages"),
    path("messages/<int:pk>/", MessageView.as_view(), name="user_messages"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
    path("bucketpoints/", BucketPointView.as_view(), name="bucket_points"),
    path("bucketpoints/<int:pk>/", BucketPointView.as_view(), name="bucket_points"),
    path("presence/", PresenceIndicatorView.as_view(), name="presence_indicator"),
    path("albums/", AlbumView.as_view(), name="albums"),
    path("albums/<int:album_id>/", AlbumView.as_view(), name="album_edition"),
    path("photos/<int:album_id>/", PhotoView.as_view(), name="photo_view"),
]
