from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

from activity.models import Activity, MultiChoice, Choice, TrueFalse, Completed, Response, get_items

class SurveySummaryView(View):
    pass


class SurveyDisplayView(View):
    pass


class SurveyItemView(View):

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
            self.template_name = 'survey/multi-choice.html'
            choices = item.choice_set.all()
            context = {'user': request.user, 'response': response, 'item': item, 'choices': choices}

        return render(request, self.template_name, context)

    def post(self, request, activity_slug, item_index):
        activity = Activity.objects.get(slug=activity_slug)
        item = get_items(activity)[item_index-1]
        if type(item) == MultiChoice:
            choices = item.choice_set.all()
            try:
                selected_choice = choices[int(request.POST['choice'])]
            except (KeyError, Choice.DoesNotExist):
                self.template_name = 'survey/multi-choice.html'
                context = {'activity':item.activity, 'item':item, 'choices':choices, 'response':None}
                context['error_message'] = 'You must choose one of the responses below.'
                return render(request, self.template_name, context)
            # make sure this user hasn't already responded to this item
            if len(Completed.objects.filter(user=request.user, activity=activity, index=item_index)) == 0:
                completed = Completed(user=request.user, activity=activity, index=item_index)
                completed.save()
                if item.privacy_type == 'AN':
                    # only need to count the votes
                    selected_choice.votes += 1
                    selected_choice.save()
                else:
                    response = Response(user=request.user, activity=activity, index=item_index,
                                        multi_choice=selected_choice)
                    response.save()

        next_page = item.next()
        print('next_page = ', next_page)
        return redirect('survey:survey_item', activity_slug, item_index)



