from django.conf import settings
from django.views.generic import DetailView, ListView

from blog.models import Blog

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/list.html'
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Блог",
        "description": "Все статьи",
    }

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    extra_context = {
        "site_name": settings.SITE_NAME,
    }
