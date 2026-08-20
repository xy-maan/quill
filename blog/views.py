from datetime import date

from django.shortcuts import render

from .models import Post

# Create your views here.


def get_date(post):
    return post.get("date")

def index(request):

    latest_posts = Post.objects.all().order_by('-date')[:3] # get latest 3 posts

    return render(request, "blog/index.html", {
        "posts": latest_posts
    })

def posts(request):

    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    })

def post_details(request, slug):
    identified_post = Post.objects.get(slug=slug)
    return render(request, "blog/post-details.html", {
        "post": identified_post,
        "tags": identified_post.tags.all()
    })
