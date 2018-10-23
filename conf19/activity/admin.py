from django.contrib import admin
from .models import Image, Activity, MultiChoice, Choice, TrueFalse, Response, Completed


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5
    readonly_fields = ('votes',)


class MultiChoiceAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class TrueFalseAdmin(admin.ModelAdmin):
    readonly_fields = ('true_count', 'false_count',)


admin.site.register(Image)
admin.site.register(Activity)
admin.site.register(MultiChoice, MultiChoiceAdmin)
admin.site.register(TrueFalse, TrueFalseAdmin)

# temp section during development
admin.site.register(Response)
admin.site.register(Completed)
