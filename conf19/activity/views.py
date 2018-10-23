from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

import datetime

from .models import Activity, MultiChoice, Choice, Completed, Response, get_items

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
            completed = len(Completed.objects.filter(user=request.user, activity=activity))
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
        completed = Completed.objects.filter(user=request.user, activity=activity.pk)
        data = []
        first_pass = True                          # this changes as soon as an incomplete page is found
        for item in items:
            if completed.filter(index=item.index) and first_pass:
                data.append((item, 'Completed'))    # If user has a response, call the page complete
            elif first_pass:
                data.append((item, 'Up next...'))   # This is the next page to do
                first_pass = False                  # after that, enter 'Pending' for the rest of the pages
            else:
                data.append((item, 'Pending'))
        return render(request, self.template_name, {'activity': activity,
                                                    'data': data,})


class DisplayView(View):

    template_name = 'activity/display.html'

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        items = get_items(activity)
        return render(request, self.template_name, {'activity': activity, 'items': items})


class ItemView(View):

    def get(self, request, activity_slug, item_index):
        activity = Activity.objects.get(slug=activity_slug)
        items = get_items(activity)
        item = items[item_index - 1]
        completed = Completed.objects.filter(user=request.user, activity=activity, index=item.index)
        responses = Response.objects.filter(user=request.user, activity=activity, index=item_index)
        try:
            response = Response.objects.get(user=request.user, activity=activity, index=item_index)
        except Response.DoesNotExist:
            response = None
        if type(item) == MultiChoice:
            self.template_name = 'activity/multi-choice.html'
            choices = item.choice_set.all()
            context = {'user': request.user, 'response': response, 'item': item, 'choices': choices}

        return render(request, self.template_name, context)

    def post(self, request, activity_slug, item_index):
        activity = Activity.objects.get(slug=activity_slug)
        item = get_items(activity)[item_index-1]
        if type(item) == MultiChoice:
            choices = item.choice_set.all()
            try:
                selected_choice = int(request.POST['choice'])
            except (KeyError, Choice.DoesNotExist):
                self.template_name = 'activity/multi-choice.html'
                context = {'activity':item.activity, 'item':item, 'choices':choices, 'response':None}
                context['error_message'] = 'You must choose one of the responses below.'
                return render(request, self.template_name, context)
            # make sure this user hasn't already responded to this item
            if len(Completed.objects.filter(user=request.user, activity=activity, index=item_index)) == 0:
                completed_by = Completed(user=request.user, activity=activity, index=item_index)
                completed_by.save()
                if item.privacy_type == 'AN':
                    user = User.objects.get(username='Anonymous')
                    response = Response(user=user, activity=activity, index=item_index,
                                        multi_choice=selected_choice)
                    response.save()
                    # need to render the next page if available
                else:
                    response = Response(user=request.user, activity=activity, index=item_index,
                                        multi_choice=selected_choice)
                if not item.opinion:
                    response.correct = selected_choice.correct
                response.save()
        return redirect('activity:item', activity_slug, item_index)
