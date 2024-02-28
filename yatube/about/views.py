from django.views.generic import TemplateView


class AuthorView(TemplateView):
    template_name = 'about/author.html'


class TechView(TemplateView):
    template_name = 'about/tech.html'
