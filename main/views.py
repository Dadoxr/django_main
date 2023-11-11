from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'main/main.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная' 
        return context
    