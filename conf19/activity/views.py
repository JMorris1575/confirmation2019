from django.shortcuts import render
from django.views import View

import datetime

from .models import Activity, Response, get_items

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



