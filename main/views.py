from django.conf import settings
from django.views.generic import TemplateView
from blog.models import Blog

from mailing.models import Recipient, Setting


class MainPageView(TemplateView):
    template_name = 'main/main.html'
    extra_context = {
        'site_name': settings.SITE_NAME,
        'title': 'Главная'
    }
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        
        context_data['all_mailings'] = Setting.objects.all().count()
        status_start = settings.NAMESETTING.get('statuses').get('status_start').get('name')
        context_data['start_mailings'] = Setting.objects.filter(status__name=status_start).count()
        context_data['all_recipients'] = Recipient.objects.all().distinct('email').count()
        context_data['random_articles'] = Blog.objects.all().order_by('?')[:3]

        return context_data
