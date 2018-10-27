from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View


class HelpView(View):

    def get(self, request):
        self.template_name = 'help/help-index.html'
        return render(request, self.template_name)
