from datetime import date

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .forms import CommentForm

# Create your views here.


def get_date(post):
    return post.get("date")

def index(request):

    latest_posts = Post.objects.all().order_by('-date')[:3] # get latest 3 posts

    return render(request, "blog/index.html", {
        "posts": latest_posts
    })

class PostsListView(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-date")


class PostDetailsView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm()
        comments = post.comments.all().order_by("-id")
        return render(request, "blog/post-details.html", {
            "post": post,
            "comment_form": comment_form,
            "tags": post.tags.all(),
            "comments": comments
        })

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if form.is_valid():
            comment = form.save(commit=False) # it doesn't save, but creates a model instance
            comment.post = post
            comment.save()
            print("\nYour Comment was saved successfully\n")
            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))
        
        return render(request, "blog/post-details.html", {
            "comment_form": form,
            "post": post,
            "tags": post.tags.all()
        })