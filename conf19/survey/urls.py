from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import SurveySummaryView, SurveyDisplayView, SurveyItemView, SurveyReportView

app_name = 'survey'

urlpatterns = [
    path('<slug:activity_slug>/summary/', login_required(SurveySummaryView.as_view()), name='summary'),
    path('<slug:activity_slug>/display/', login_required(SurveyDisplayView.as_view()), name='display'),
    path('<slug:activity_slug>/<int:item_index>/', login_required(SurveyItemView.as_view()), name='item'),
    path('report/<slug:activity_slug>/<int:item_index>/', login_required(SurveyReportView.as_view()), name='report',)
]