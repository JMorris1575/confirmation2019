from django.contrib import admin
from .models import Image, Activity, MultiChoice, Choice, TrueFalse, Response, Completed


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5
    readonly_fields = ('votes',)


class MultiChoiceAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    actions = ['clear_votes']

    def clear_votes(self, request, queryset):
        for item in queryset:
            choices = item.choice_set.all()
            choices.update(votes=0)
        rows_updated = len(queryset)
        if rows_updated == 1:
            message_bit = '1 item was'
        else:
            message_bit = '%s items were' % rows_updated
        self.message_user(request, '%s successfully cleared.' % message_bit)
    clear_votes.short_description = "Set votes to zero for all choices on selected items"


class TrueFalseAdmin(admin.ModelAdmin):
    readonly_fields = ('true_count', 'false_count',)
    actions = ['clear_counts']

    def clear_counts(self, request, queryset):
        rows_updated = queryset.update(true_count=0, false_count=0)
        if rows_updated == 1:
            message_bit = '1 item was'
        else:
            message_bit = '%s items were' % rows_updated
        self.message_user(request, '%s successfully cleared.' % message_bit)
    clear_counts.short_description = "Set true/false counts to zero on selected items"



admin.site.register(Image)
admin.site.register(Activity)
admin.site.register(MultiChoice, MultiChoiceAdmin)
admin.site.register(TrueFalse, TrueFalseAdmin)

# temp section during development
admin.site.register(Response)
admin.site.register(Completed)
