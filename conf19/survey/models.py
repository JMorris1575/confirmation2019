from django.db import models
from activity.models import Item, MultiChoice, Choice, TrueFalse, Response

class SurveyItem(Item):
    pass


class SurveyMultiChoice(MultiChoice):
    pass


class SurveyChoice(Choice):
    votes = models.PositiveIntegerField(default=0)


class SurveyTrueFalse(TrueFalse):
    true_count = models.PositiveIntegerField(default=0)
    false_count = models.PositiveIntegerField(default=0)


class SurveyResponse(Response):
    pass