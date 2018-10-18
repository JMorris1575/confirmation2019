from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import WelcomeView, SummaryView, DisplayView, ItemView

app_name = 'activity'

urlpatterns = [
    path('', RedirectView.as_view(url='/activity/welcome/')),
    path('welcome/', login_required(WelcomeView.as_view()), name='welcome'),
    path('<slug:activity_slug>/summary/', login_required(SummaryView.as_view()), name='summary'),
    path('<slug:activity_slug>/display/', login_required(DisplayView.as_view()), name='display'),
    path('<slug:activity_slug>/<int:item_index>/', login_required(ItemView.as_view()), name='item'),
]