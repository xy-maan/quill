from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index-page"),
    path("posts/", views.PostsListView.as_view(), name="posts-page"),
    path("posts/<slug:slug>/", views.PostDetailsView.as_view(), name="post-details-page"),
    path("read-later"),
]
