from django.contrib import admin
from .models import Image, Activity, Item, MultiChoice, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class MultiChoiceAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Image)
admin.site.register(Activity)
admin.site.register(Item)
admin.site.register(MultiChoice, MultiChoiceAdmin)


