import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponseServerError


class GameView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        # handles get requests. Renders webpage based on index.html template
        context = self.get_context_data(**kwargs)

        return TemplateResponse(
            request,
            self.template_name,
            context
        )