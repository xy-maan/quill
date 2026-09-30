from datetime import date

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post

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


class PostDetailsView(DetailView):
    template_name = "blog/post-details.html"
    model = Post
    context_object_name = "post"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = self.object.tags.all()
        return context