from django.shortcuts import render
from django.views import View

import datetime

from .models import Activity, MultiChoice, Response, get_items

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.filter(publish_date__lte=datetime.date.today(),
                                             closing_date__gt=datetime.date.today(),
                                             visible=True)
        data = []
        for activity in activities:
            items = get_items(activity)
            item_count = len(items)
            completed = len(Response.objects.filter(user=request.user, activity=activity, completed=True))
            if item_count != 0:
                percent_completed = completed/item_count * 100
                if percent_completed < 100:
                    msg = '{:.1f}'.format(percent_completed) + '% Complete'
                else:
                    msg = 'Finished!'
            else:
                msg = 'Not Yet Available'
            data.append((activity, msg))
        return render(request, self.template_name,
                      {'data': data})


class SummaryView(View):
    template_name = 'activity/summary.html'

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        items = get_items(activity)
        responses = Response.objects.filter(user=request.user, activity=activity.pk)
        data = []
        first_pass = True                          # this changes as soon as an incomplete page is found
        for item in items:
            if responses.filter(index=item.index) and first_pass:
                data.append((item, 'Completed'))    # If user has a response, call the page complete
            elif first_pass:
                data.append((item, 'Up next...'))   # This is the next page to do
                first_pass = False                  # after that, enter 'Pending' for the rest of the pages
            else:
                data.append((item, 'Pending'))
        return render(request, self.template_name, {'activity': activity,
                                                    'data': data,})


class ItemView(View):

    def get(self, request, activity_slug, item_index):
        activity = Activity.objects.get(slug=activity_slug)
        items = get_items(activity)
        item = items[item_index]
        responses = Response.objects.filter(user=request.user, activity=activity, index=item.index)
        response = None
        if len(responses) == 1:
            response = responses[0]
        if type(item) == MultiChoice:
            self.template_name = 'activity/multi-choice.html'
            choices = item.choice_set.all()
            context = {'user': request.user, 'activity': activity, 'response': response, 'item': item, 'choices': choices}

        return render(request, self.template_name, context)

    def post(self, request, activity_slug, item_index):
        pass









