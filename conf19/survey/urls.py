from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import SurveySummaryView, SurveyDisplayView, SurveyItemView

app_name = 'survey'

urlpatterns = [
    path('<slug:activity_slug>/summary/', login_required(SurveySummaryView.as_view()), name='survey_summary'),
    path('<slug:activity_slug>/display/', login_required(SurveyDisplayView.as_view()), name='survey_display'),
    path('<slug:activity_slug>/<int:item_index>/', login_required(SurveyItemView.as_view()), name='survey_item'),
]