from django.contrib import admin
from .models import SurveyMultiChoice, SurveyChoice, SurveyTrueFalse, SurveyResponse


class SurveyChoiceInline(admin.StackedInline):
    model = SurveyChoice
    extra = 5
    readonly_fields = ('votes',)

class SurveyMultiChoiceAdmin(admin.ModelAdmin):
    inlines = [SurveyChoiceInline]


class SurveyTrueFalseAdmin(admin.ModelAdmin):
    readonly_fields = ('true_count', 'false_count',)


admin.site.register(SurveyMultiChoice, SurveyMultiChoiceAdmin)
admin.site.register(SurveyTrueFalse, SurveyTrueFalseAdmin)

