from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import HelpView

app_name = 'help'

urlpatterns = [
    path('', RedirectView.as_view(url='index/')),
    path('index/', HelpView.as_view(), name='index'),
]