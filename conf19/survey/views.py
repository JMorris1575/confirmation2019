from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

from activity.models import Activity, MultiChoice, Choice, TrueFalse, Completed, Response, get_items

def get_navigation_context(item, activity, modifier, context):
    """
    Returns the urls for the previous and next pages
    :param item: the item being displayed along with its app_name
    :param activity: the activity the item belongs to with its slug
    :param modifier: the third part of the url or an empty string ('report/' for instance, or '')
    :param context: the context variable to be modified
    :return: None, but the context variable now has two new fields 'previous_url' and 'next_url'
    """
    navigation_info = item.get_navigation_info()
    previous_url = None
    next_url = None
    if navigation_info:
        previous_info = navigation_info['previous_info']
        if previous_info:
            previous_url = '/' + previous_info['app_label'] + '/' + modifier + activity.slug + '/' + str(
                previous_info['index'])
        next_info = navigation_info['next_info']
        if next_info:
            next_url = '/' + next_info['app_label'] + '/' + modifier + activity.slug + '/' + str(next_info['index'])
    context['previous_url'] = previous_url
    context['next_url'] = next_url


class SurveySummaryView(View):
    pass


class SurveyDisplayView(View):
    pass


class SurveyItemView(View):

    def get(self, request, activity_slug, item_index):
        activity = Activity.objects.get(slug=activity_slug)
        items = get_items(activity)
        item = items[item_index - 1]    # get the item associated with item_index
        if not item.allowed(request.user, items, item_index):
            return redirect('activity:summary', activity_slug)
        try:
            completed = Completed.objects.get(user=request.user, activity=activity, index=item.index)
        except Completed.DoesNotExist:
            completed = None
        responses = Response.objects.filter(user=request.user, activity=activity, index=item_index)
        if len(responses) == 1:         # discussions may have more than one response
            response = responses[0]     # if there is only one response, remember it
        else:
            response = None             # otherwise set the response to None
        context = {'user': request.user, 'completed': completed, 'response': response, 'item': item}
        if type(item) == MultiChoice:
            self.template_name = 'survey/multi-choice.html'
            choices = item.choice_set.all()
            context['choices'] = choices
            get_navigation_context(item, activity, '', context)
        elif type(item) == TrueFalse:
            self.template_name = 'survey/true-false.html'
            get_navigation_context(item, activity, '', context)

        return render(request, self.template_name, context)

    def post(self, request, activity_slug, item_index):
        activity = Activity.objects.get(slug=activity_slug)
        items = get_items(activity)
        item = items[item_index - 1]
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
        elif type(item) == TrueFalse:
            try:
                selected_response = request.POST['choice']
            except (KeyError):
                self.template_name = 'survey/true-false.html'
                context = {'activity':item.activity, 'item':item}
                context['error_message'] = 'You must select either True or False.'
                return render(request, self.template_name, context)
            # make sure this user hasn't already responded to this item
            if len(Completed.objects.filter(user=request.user, activity=activity, index=item_index)) == 0:
                completed = Completed(user=request.user, activity=activity, index=item_index)
                completed.save()
                if item.privacy_type == 'AN':
                    # only need to count the votes
                    if selected_response == 'true':
                        item.true_count += 1
                    else:
                        item.false_count += 1
                    item.save()
                else:
                    response = Response(user=request.user, activity=activity,
                                        index=item_index, true_false=selected_response=='true')
                    response.save()

        navigation_info = item.get_navigation_info()
        if navigation_info:
            next_item_info = navigation_info['next_info']
            if next_item_info:
                return redirect('/' + next_item_info['app_label'] + '/' +
                                activity_slug + '/' + str(next_item_info['index']) + '/')
        return redirect('activity:welcome')


class SurveyReportView(View):

    def get(self, request, activity_slug, item_index):
        activity = Activity.objects.get(slug=activity_slug)
        items = get_items(activity)
        item = items[item_index - 1]
        context = {'user':request.user, 'item':item, 'completed':True}      # completed is used by navigation.html
        get_navigation_context(item, activity, 'report/', context)
        if type(item) == MultiChoice:
            self.template_name = 'survey/multi-choice-report.html'
            choices = item.choice_set.all()
            context['choices'] = choices
        elif type(item) == TrueFalse:
            self.template_name = 'survey/true-false-report.html'
            total = item.true_count + item.false_count
            if total != 0:
                percent_true = round(item.true_count * 100 / total)
                percent_false = round(item.false_count * 100 / total)
            else:
                percent_true = 0
                percent_false = 0
            context['percent_true'] = percent_true
            context['percent_false'] = percent_false
        return render(request, self.template_name, context)

