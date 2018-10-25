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
        try:
            completed = Completed.objects.get(user=request.user, activity=activity, index=item.index)
        except Completed.DoesNotExist:
            completed = None
        # responses = Response.objects.filter(user=request.user, activity=activity, index=item_index)
        try:
            response = Response.objects.get(user=request.user, activity=activity, index=item_index)
        except Response.DoesNotExist:
            response = None
        if type(item) == MultiChoice:
            self.template_name = 'survey/multi-choice.html'
            choices = item.choice_set.all()
            context = {'user': request.user, 'completed': completed, 'response': response,
                       'item': item, 'choices': choices}
        elif type(item) == TrueFalse:
            self.template_name = 'survey/true-false.html'
            context = {'user': request.user, 'completed': completed, 'response': response, 'item': item}

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

        print('item_index = ', item_index)
        next_item_index = item.next()
        print('next_item_index = ', next_item_index)
        if next_item_index:
            print('items = ', items)
            new_item = items[next_item_index - 1]
            return redirect('/' + new_item.get_item_type_display() + '/' + activity_slug + '/' + str(next_item_index) + '/')
        else:
            return redirect('activity:welcome')



