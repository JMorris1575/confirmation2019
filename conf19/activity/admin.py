from django.contrib import admin
from .models import Image, Activity, Item, MultiChoice, Choice, TrueFalse, Response, CompletedBy


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5


class MultiChoiceAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Image)
admin.site.register(Activity)
admin.site.register(MultiChoice, MultiChoiceAdmin)
admin.site.register(TrueFalse)

# temp section during development
admin.site.register(Response)
admin.site.register(CompletedBy)
