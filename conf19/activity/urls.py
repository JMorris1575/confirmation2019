from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import WelcomeView

app_name = 'activity'

urlpatterns = [
    path('', RedirectView.as_view(url='/activity/welcome/')),
    path('welcome/', login_required(WelcomeView.as_view()), name='welcome'),
]