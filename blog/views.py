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
        stored_posts = request.session.get("stored_posts")

        is_read_later = False

        if post.id in stored_posts:
            is_read_later = True

        return render(request, "blog/post-details.html", {
            "post": post,
            "comment_form": comment_form,
            "tags": post.tags.all(),
            "comments": comments,
            "is_read_later": is_read_later
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

class ReadLaterView(View):

    def get(self, request):

        stored_posts = request.session.get("stored_posts")

        has_posts = False

        posts = []

        if stored_posts is not None:
            has_posts = True
            # for post_id in stored_posts:
            #     posts.append(Post.objects.get(id=post_id))
            posts = Post.objects.filter(id__in=stored_posts)

        return render(request, "blog/read-later.html", {
            "posts": posts,
            "has_posts": has_posts
        })

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse("index-page"))
