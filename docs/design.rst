==================================
Designing Confirmation2019 Website
==================================

I'm going to take a more gradual approach this year and hopefully I will be able to get something done before the end of
the year!

I have been working on the website, its header, footer, login and logout pages, with the idea of learning Bootstrap 4.
It's looking fairly good and is much more responsive than what I had last year, but I don't want to start with such a
complex site as I was working on then. To start I will try to create a survey based on Matthew Kelly's "The Biggest Lie
in the History of Christianity."

When users log in to the website they will arrive at a Welcome page which explains the purpose of the survey and that
their identity will not be saved with their entries and are strictly confidential. There will be a button on the page
to allow them to enter the survey. They will enter answers one question at a time. I will suggest they don't overthink
their answers with the idea that their first impression is likely to be more appropriate. Once an answer is submitted it
cannot be changed since their identities are not being saved. If any users have to quit before completing the entire
survey they can return to it later at the question where they left off.

Thinking Through the Model Design
=================================

Initial Thoughts
----------------

I'm thinking there should be a manager app and a separate app for every type of question: true/false, multiple choice,
discussion, etc. This is different than what I did last year, and I haven't thought it through yet, but I'm hoping it
will make for a simpler design.

The manager app will be something like the activity app last year in that it is the launching point for each of the
activities. The difference will be that each of the apps for the individual question types will handle its own work and
the manager app will only have to keep track of which units/questions go into each activity.

Looking at Last Year
--------------------

Last year I had the following models in the Activity app:

#. Image - which held the filename of the image and a category field but I don't remember what it did.

#. Activity - which held an index to keep it in order, a name and a slug, overview text and an optional image
   as well as optional publish and close dates and a field to indicate whether the activity should be visible.

#. Page - this held the complexity I am trying to avoid by using separate models for all the different question types.
   It did, however, contain some methods to return the next page or previous page if there was one, and if the user
   was allowed to access it. I'm not sure where to put that in this new approach. A mixin perhaps?

#. Response - which also carried a level of complexity due to the fact that it included responses to many different
   types of questions.

#. Choice - which contained the possible choices for multiple choice questions.

Perhaps I don't need a lot of separate apps but a lot of separate models for the different kinds of questions instead of
trying to stuff them all into one page model. Each one could have certain fields in common, perhaps these could come
from a common inherited class.

A Start for This Year
---------------------

To start with I will only need a survey activity and a couple of question types: multi-choice and true-false. The
commonly inherited class could have the index field, the user field, the activity foreign key, and perhaps other common
fields I may want to have later, like a boolean field indicating whether the question has a correct answer to be
displayed (which none of the survey questions would.)

Here is a first draft of the models:

**Activity**

#. index, a PositiveSmallIntegerField marked as unique
#. name, the name of the activity in a CharField of 100 characters or less
#. slug, a slug field to use in creating a url for the activity
#. overview, a long CharField (512 characters or less) describing the activity

**Page**

(The commonly inherited class)

#. activity, a ForeignKey to the activity model
#. index, a PositiveSmallIntegerField to keep the questions in order and help find previous and next pages

**Multi_Choice**

(inherits Page)

#. text, a long CharField (512 characters) to hold the question being asked

**Choice**

multi_choice, a ForeignKey to the corresponding Multi_Choice question
index, a PositiveSmallIntegerField to keep the choices in order
text, a CharField containing one of the choices for this question
correct, a boolean field indicating whether this is the correct response or null if there is no correct response

**True_False**

(inherits Page)

#. text, a long CharField (512 characters) with the statement to be evaluated
#. correct, a boolean field giving the correct response if any

Remembering User Responses
--------------------------

Last year I used the Responses model as defined below::

    class Response(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
        page = models.ForeignKey(Page, on_delete=models.CASCADE)
        created = models.DateTimeField(auto_now_add=True)
        last_edited = models.DateTimeField(auto_now=True)
        essay = models.TextField(blank=True)
        multi_choice = models.PositiveSmallIntegerField(null=True, blank=True)
        true_false = models.BooleanField(default=False)
        correct = models.NullBooleanField(null=True)
        completed = models.BooleanField(default=False)

        class Meta():
            ordering = ['created']

        def __str__(self):
            name = self.user.first_name + ' ' + self.user.last_name
            if name[-1] == 's':
                possessive_ending = "'"
            else:
                possessive_ending = "'s"
            return name + possessive_ending + ' response to ' + str(self.page)

        def is_correct(self):
            return self.correct

        def can_delete(self):
            """
            Returns True if this response can be deleted, false otherwise
            A response can be deleted if it's answer has not been revealed and if the user has not completed any pages
            beyond this one in the current activity
            :return: boolean
            """
            this_index = self.page.index
            number_completed = len(Response.objects.filter(user=self.user, activity=self.activity))
            if (this_index == number_completed) and not self.page.reveal_answer:
                return True
            else:
                return False

        def can_goto_next(self):
            """
            Returns true if this user has completed this page and so can go to the next
            :return: boolean
            """
            return self.completed

        def user_choice(self):
            return Choice.objects.get(page=self.page, index=int(self.multi_choice))

This cannot be used as such this year as long as my ``Item`` class (the replacement for ``Page``) is an abstract class.
Abstract classes cannot be used as foriegn keys. It seems I should, however, be able to save the index each item has in
the activity (``activity`` and ``index`` should probably be defined as ``unique_together`` by the way) and use that to
find the appropriate item whether it be a MultiChoice, TrueFalse, or other sorts of items to be defined later.

Getting All of an Activity's Items
----------------------------------

But thinking about that raised another question in my mind. If each sort of item is to be in a separate model how are
the templates and any methods that need to locate them going to know which kind of item to locate. Should I have an
additional field in the ``Item`` class for that? It could use the same ``choices`` field option that I did last year.

But that begs the question. I would have to select, or set as a constant, an ``item_type`` in each model but I wouldn't
be able to check that field until I had already retrieved that item. There must be some sort of way I can collect all
of the items that go with an activity and present them in a sorted list or query_set...

I think I will create the TrueFalse model and practice in the shell.

...

After creating the TrueFalse model, some practice, reading the Djago docs about filters, and some more thought, I think
it will work to create a global method in ``activity.models.py`` to return a sorted list of items for a given activity.
I'm not sure how it will get sorted but I'll play with it for a while in the shell to figure it out.

...

It turned out to be quite simple, but it took a lot of experimentation and study to figure it out. It turns out there is
an import from Python that does the main part of the work::

    def get_items(activity):
        """
        Returns a sorted QuerySet of all the items of various sorts included in activity
        :param activity: the activity whose items are to be found
        :return: a QuerySet of all items sorted according to their index
        """
        def get_index(x):
            return x.index

        mc = activity.multichoice_set.all()
        mc_list = list(mc)
        tf = activity.truefalse_set.all()
        tf_list = list(tf)
        return list(merge(mc_list, tf_list, key=get_index))

To use it within the model class just write code such as the following::

    activity = Activity.objects.get(pk=15)
    item_list = get_items(activity)

To use it in views I imagine there will have to be an import line such as::

    from activity.models import get_items

Or I could just import everything::

    from activity.models import *

Thinking About the Response Model
----------------------------------

In trying to implement the post() method for the ItemView for MultiChoice items I realized that I need to rethink the
Response Model. I need to be able to keep track of which items a particular user has completed but I don't always want
to associate that user with their response. This suggests that I may need two models, one for Completions and the other
for the actual responses. The completions can be recorded with the actual user, the Responses can be recorded with the
actual user or with an anonymous user (who I will have to invent in the admin as one of the auth.users.)

This also reinforces something I have known for some time, that the Item model, inherited by the models for the
different item types, will have to include more information than it currently does. For instance, whether the response
is supposed to be Public, Anonymous, or Semi-anonymous.

It may be convenient to put a ``votes`` field in the MultiChoice model but that may not really be necessary. I think I
can devise other ways to count them.

By the way, last year's version of the Response model contained a ``completed`` boolean field. I'm not sure why, it
seems that if there IS a response from that user for a particular activity and item, it would ALWAYS be marked ``True``.
Why bother? Just create the Response and that, in itself, shows that there was one!

Addition to the Response Model
------------------------------

Here is the code from last year concerning the various types of discussions::

    discussion_type = models.CharField(max_length=20,   # indicates type of discussion
                                       choices=[('OP', 'Open'),
                                                ('SA', 'Semi-Anonymous'),
                                                ('AN', 'Anonymous')],
                                       blank=True,
                                       default='')

I am thinking of changing it to the following::

    privacy_type = models.CharField(max_length=2,   # indicates privacy level of an item
                                    choices=[('OP', 'Open'),               # responder able to be openly published
                                             ('SA', 'Semi-Anonymous'),     # responder only visible to team members
                                             ('AN', 'Anonymous')],         # responder not saved
                                    default='OP')

Before I do this I should think clearly through how this will affect the processing of the responses...

+--------------+---------------------------------------------------------------------------------------------+
| privacy_type | Handling                                                                                    |
+==============+=============================================================================================+
|   'OP'       | Items marked 'OP' are open for publication. User is saved to Completed and to Responses.    |
+--------------+---------------------------------------------------------------------------------------------+
|   'SA'       | Items marked 'SA' are semi-anonymous. User is saved to Completed and to Responses but the   |
|              | pages that publicly display responses will not include the user's name. Only team members   |
|              | can access a page that reveals both response and the user's name. I will have to develop a  |
|              | special /team/ url.                                                                         |
+--------------+---------------------------------------------------------------------------------------------+
|   'AN'       | Items marked 'AN' are anonymous. For some items, such as MultiChoice and TrueFalse, the     |
|              | User is saved to Completed but something like FakeUser is saved to Responses. For others,   |
|              | such as Discussion and perhaps Essay items, no record is even kept in Completed.            |
+--------------+---------------------------------------------------------------------------------------------+

Dealing with Different Item Types
---------------------------------

While working on implementing the behavior of the program after posting an Anonymous ('AN') MultiChoice response I
discovered that my thinking has not been too clear on the subject. I was trying to get the program to display the user's
response for possible editing but, of course, if their response was properly saved anonymously there would be no way to
do that. The current user's response could not be distinguished from the others with the same activity and item index.

That led me to think about where the logic for deciding what to do in each case should reside: the view, the .html page
or the model? Thinking of the addage about fat models and skinny views got me to thinking of a simpler way to save the
user information with the response: have the view call a ``stored_user`` method of the ``Item`` class which could
check on the value of ``privacy_type`` and return either the request.user or the anonymous user (currently called
Anonymous I believe).

The logic for what gets displayed: a review page giving a chance to edit or a page displaying the next item up for
completion still makes sense in the view it seems to me. I'm thinking that, for 'AN' items the program will have to
figure out whether there IS a next page and, if so, go to it, otherwise go back to the summary page. It would be nice
to create some kind of thank-you page with the possibility of displaying a ``closing_message`` (from the Item model)
which would display and then, when dismissed, bring the user back to the welcome page. I'm thinking this would involve
creating a new kind of item model: a ClosingMessage model to store and display this message.

Thinking Trough the Process of Item get() and post()
====================================================

I'm having a bad time with the ItemView get() and post() methods because I haven't thought this through. There are
several things to consider: whether this is the first time get() is entered in order to display the input form or if the
input form has just been filled out and posted and this entry is to display the user's response for possible editing.
Also, it makes a difference whether the item in question is marked 'AN' for Anonymous or not. Here is an attempt to
follow the necessary logic and obtain what needs to be obtained for the template:

#. User clicks on the button on the summary page to respond to the item in question.
#. In ItemView.get(), user, activity and item_index are known, but this item is not marked completed by this user.
#. The input form appears allowing the user to respond.
#. In ItemView.post() user, acivity and item_index are known along with the users response. The item is marked as being
   CompletedBy this user and, if the item is 'OP' or 'SA' the user's identity is saved with the response. If the item is
   'AN', the Anonymous User is stored with the response.
#. ItemView.post() redirects to ItemView.get() where user, acivity and item_index are known. This time the user has a
   CompletedBy entry for this item.

   A. If the item is marked 'AN' the user goes automatically to the next item. If the next
      item is the closing page for the activity the user goes from there back to the welcome page.
   #. If the item is marked 'OP' or 'SA' the user will be given an opportunity to edit his or her response. Since there
      is a response listed for this user it can be sent to the template. If the item is a discussion item, the user is
      simply directed to the discussion display page where there is automatically an opportunity for a user to edit his
      or her entries.

This suggests that the logic for figuring out what to do needs to be in the ItemView rather than in the template,
though the template will have to have it's own logic to determine what to display.

A Major Refactoring
===================

This whole process seems just too complex. I'm thinking it may have been better after all to divided the functions of
this program into a larger number of Django apps and better keep to the ideal of each app doing just one thing and doing
it well.

Right now my activity app is trying to do most all of the work. I may want, instead, to have it manage a list of items
and have the items of various kinds each have their own apps. Thus I could have a survey app that has its own models
for survey items, all subclassing the Item model from the activity app. Perhaps the activity app can keep generic
models of various sorts of activities, such as MultiChoice, TrueFalse, Essay, Discussion, and each of the apps, like
the survey app, could have its own models derive from them. A diagram of all these relationships could be helpful as
I try to figure it all out.

Meanwhile, I'd like to have a way to quickly print out my whole survey01 activity, questions and answers, since I am
probably going to have to delete and recreate the conf19 database. Perhaps I will do that first.

Rescuing the Data from the Database
-----------------------------------

Well, not really rescuing it, just printing it out so it can be re-entered. I want to interate through the items in
the activity and display them on an html page. This will require a new urlconf for the activity app, a new view, and
a new html template.

The urlconf can be ``activity/<activity.slug>/display``

The new view can be called ``DisplayView``, subclass ``View`` and have to override only the get() method. It may have to
collect quite a bit of information to send through the ``context`` variable or the template language may be
sophisiticated enough to get what it needs just from the activity. (``{% for item in activity.item_set %}`` for
instance, and each model may know how to gather a list of display lines to be formatted by the template.

The new template can be called ``display.html`` and, once it is displayed, be printed through the browser.

...

That worked out fairly well. I couldn't do the ``{% for item in activity.item_set %}`` thing though. I might have been
able to if I'd worked at it long enough, or created a method in the Activity model to supply the associated set of
items. It was easier just to add the items to the context variable in the view.

I did have to print a version of the page shrunk down to 44% of its size to get what is really three html pages
header.html, display.html and footer.html, to print on one sheet. Printing is a topic for later study. It's not of great
concern to me now.

Rethinking the Apps
===================

Here is a chart of various apps and their duties as I now conceive them:

+--------------+-------------------------------------------------------------------------------------------------------+
|   App Name   |                                                Duties                                                 |
+==============+=======================================================================================================+
| activity     | #. Define the ``Activity``, ``Image``, ``Item``, ``ResponseGeneric`` and ``CompletedBy`` models; and  |
|              |    generic models of all possible item types.                                                         |
|              | #. Define the ``Activity`` model to include:                                                          |
|              |                                                                                                       |
|              |    A. ``index``, ``name``, ``slug``, ``overview``, ``image``, ``publish_date``, ``closing_date``, and |
|              |       visible fields.                                                                                 |
|              |    #. a ``get_items()`` method to retrieve the items for this activity.                               |
|              |                                                                                                       |
|              | #. Define the ``Item`` model to include:                                                              |
|              |                                                                                                       |
|              |    A. ``activity``, ``index``, ``title``, ``privacy_type``, ``opinion``, ``reveal_answer`` and        |
|              |       ``visible`` fields.                                                                             |
|              |    #. ``previous()`` and ``next()`` methods to handle paging [may require permission calls to child   |
|              |       models].                                                                                        |
|              |                                                                                                       |
|              | #. Define the ``Image`` model, before the ``Activity`` model, to include filename and category.       |
|              | #. Define the ``GenericResponse`` model to include:                                                   |
|              |                                                                                                       |
|              |    A. ``user``, ``activity`` and ``item_index`` fields.                                               |
|              |    #. know that ``user`` here may end up to be ``Anonymous User``.                                    |
|              |                                                                                                       |
|              | #. Define the ``CompletedBy`` model to include:                                                       |
|              |                                                                                                       |
|              |    A. ``user``, ``activity``, ``created`` and ``last_edited`` fields.                                 |
|              |    #. any methods that become necessary in this new approach.                                         |
|              |                                                                                                       |
|              | #. Define the generic models, such as ``MultiChoice``, ``TrueFalse``, ``Essay`` and ``Discussion`` as |
|              |    follows:                                                                                           |
|              |                                                                                                       |
|              |    A. ``MultiChoiceGeneric`` (subclassing ``Item``):                                                  |
|              |                                                                                                       |
|              |       i. Define a ``text`` field to contain the prompt or question.                                   |
|              |       #. Define ``get_text()``, ``get_choices()`` and ``get_subtext()`` methods.                      |
|              |                                                                                                       |
|              |    #. ``TrueFalseGeneric`` (subclassing ``Item``):                                                    |
|              |                                                                                                       |
|              |       i. Define a ``statement`` field.                                                                |
|              |       #. Define ``get_text()`` and ``get_subtext()`` methods.                                         |
|              |                                                                                                       |
|              |    #. ``EssayGeneric`` (subclassing ``Item``):                                                        |
|              |                                                                                                       |
|              |       i. Define a ``text`` field to contain the prompt or question.                                   |
|              |       #. Define ``get_text()`` and ``get_subtext()`` methods. (``get_subtext`` returns ["Essay"]      |
|              |                                                                                                       |
|              |    #. ``DiscussionGeneric`` (subclassing ``Item``):                                                   |
|              |                                                                                                       |
|              |       i. Define a ``text`` field to contain the prompt or question.                                   |
|              |       #. Define ``get_text()`` and ``get_subtext()`` methods. (``get_subtext`` returns ["Discussion"] |
|              |                                                                                                       |
|              | #. Define ``WelcomeView``, ``SummaryView``, ``DisplayView`` and ``ItemView`` view classes all         |
|              |    subclassing ``View``.                                                                              |
|              |                                                                                                       |
|              |    A. The ``WelcomeView``, ``SummaryView`` and ``DisplayView`` will work much as they do now.         |
|              |    #. The ``ItemView`` will simply dispatch each item to its own app for processing.                  |
+--------------+-------------------------------------------------------------------------------------------------------+
| multi_choice | #. Define ``MultiChoice`` and ``MCResponse`` models.                                                  |
|              | #. Define the ``MultiChoice`` model, subclassing ``MultiChoiceGeneric`` to include:                   |
|              |                                                                                                       |
|              |    A. ``explanation`` to be revealed if ``reveal_answer`` is True. (optional field)                   |
|              |    #. any new methods that may be necessary.                                                          |
|              |                                                                                                       |
|              | #. Define the ``MCResponse``, subclassing ``ResponseGeneric``, to include:                            |
|              |                                                                                                       |
|              |    A. a ``user_choice`` field to store the user's response.                                           |
|              |    #. any new methods that may be necessary.                                                          |
|              |                                                                                                       |
|              | #. The MultiChoiceView, subclassing View, on:                                                         |
|              |                                                                                                       |
|              |    A. ``get()`` should:                                                                               |
|              |                                                                                                       |
|              |       i. if no previous response has been made, displays the text with its choices in a form          |
|              |       #. if a previous response has been made:                                                        |
|              |                                                                                                       |
|              |          a. if it is not an opinion item and the answer is to be revealed, gives the answer           |
|              |          #. if it is not an opinion item and the answer is not to be revealed simply displays the     |
|              |             user's choice and offers the chance to edit the response.                                 |
|              |          #. if it is an opinion item, the user's choice is revealed and can be edited.                |
|              |                                                                                                       |
|              |    B. ``post()`` should:                                                                              |
|              |                                                                                                       |
|              |       i. send an error back if the user made no selection                                             |
|              |       #. record the user's choice with his or her identity and redirect to the same page.             |
|              |                                                                                                       |
|              | #. The MultiChoiceEditView, subclassing View, on:                                                     |
|              |                                                                                                       |
|              |    A. ``get()`` should: redisplay the input form with the user's previous choice already marked.      |
|              |                                                                                                       |
|              |    #. ``post()`` should: find the user's old choice and change it to the new choice.                  |
+--------------+-------------------------------------------------------------------------------------------------------+
| true_false   | #. Define ``TrueFalse`` and ``TFResponse`` models.                                                    |
|              | #. Define the ``TrueFalse`` model, subclassing ``TrueFalseGeneric`` to include:                       |
|              |                                                                                                       |
|              |    A. ``correct_response`` for items that are not marked opinion.                                     |
|              |    #. any new methods that may be necessary.                                                          |
|              |                                                                                                       |
|              | #. Define the ``TFResponse`` model, subclassing ``ResponseGeneric``, to include:                      |
|              |                                                                                                       |
|              |    A. a ``user_response`` boolean field to store the user's response.                                 |
|              |    #. any new methods that may be necessary.                                                          |
|              |                                                                                                       |
|              | #. Define the views here.                                                                             |
+--------------+-------------------------------------------------------------------------------------------------------+
| survey       | #. Define ``SurveyMC`` and ``SurveyTF`` models.                                                       |
|              | #. Define the ``SurveyMC`` model, subclassing ``MultiChoiceGeneric``, to include nothing new.         |
|              | #. Define the ``SurveyChoices`` model, subclassing ``ChoiceGeneric``, to include:                     |
|              |                                                                                                       |
|              |    A. ``vote_count`` to store the number of votes for that choice.                                    |
|              |    #. any new methods that may be necessary.                                                          |
|              |                                                                                                       |
|              | #. Define the ``SurveyTF`` model, subclassing ``TrueFalse`` to include:                               |
|              |    A. ``true_votes`` and ``false_votes`` to keep track of the statistics.                             |
|              |    #. any new methods that may be necessary.                                                          |
|              |                                                                                                       |
|              | #. Define the views here.                                                                             |
+--------------+-------------------------------------------------------------------------------------------------------+
| essay        | #. Define ``Essay`` and ``EssayResponse`` models.                                                     |
+--------------+-------------------------------------------------------------------------------------------------------+
| discussion   | #. Define ``Discussion`` and ``DiscussionResponse`` models.                                           |
+--------------+-------------------------------------------------------------------------------------------------------+
| challenge    | #. Define ``Challenge`` and ``ChallengeResponse`` models.                                             |
+--------------+-------------------------------------------------------------------------------------------------------+

This is also getting very complex. Perhaps I should keep what I have but create a separate ``survey`` app with models
and views developed something like what is described for the ``status`` app above.

Creating the Survey App
=======================

I have been thinking about it and it seems that I will need a new ``urls.py`` in this app as well as ``views.py`` to
handle the new views. The ``models.py`` file will need to modify the already existing ``Choices`` model to include
``votes``, the ``TrueFalse`` model to include ``true_votes`` and ``false_votes`` and perhaps I should add a ``SurveyMC``
model just for completeness. The ``SurveyResponses`` model, subclassing ``Response``, can be available if I ever want
to do a survey where the users are identified with their votes.

I start with: ``python manage.py startapp survey``

Right-clicking the new ``survey`` folder I added all its files to be tracked by Git.

I created a ``urls.py`` file and added::

    from django.urls import path
    from django.contrib.auth.decorators import login_required
    from django.views.generic import RedirectView
    from .views import SurveySummaryView, SurveyDisplayView, SurveyItemView

    app_name = 'survey'

    urlpatterns = [
        path('<slug:activity_slug>/summary/', login_required(SurveySummaryView.as_view()), name='survey_summary'),
        path('<slug:activity_slug>/display/', login_required(SurveyDisplayView.as_view()), name='survey_display'),
        path('<slug:activity_slug>/<int:item_index>/', login_required(SurveyItemView.as_view()), name='survey_item'),
    ]

I added empty view classes to be imported as shown above.

I updated ``config.urls.py`` to include ``path('survey/', include('survey.urls')),``

In ``survey.models.py`` I added::

    from django.db import models
    from activity.models import Item, MultiChoice, Choice, TrueFalse, Response

    class SurveyItem(Item):
        pass


    class SurveyMultiChoice(MultiChoice):
        pass


    class SurveyChoice(Choice):
        pass


    class SurveyTrueFalse(TrueFalse):
        pass


    class SurveyResponse(Response):
        pass

Looking over these proposed models, however, I got to wondering if I really need a ``SurveyItem`` model in the models
or if I need anything more than a ``SurveyItemView`` in the views. I will leave the doubtful classes empty as I begin
to implement the ``survey`` app.

Here is what I'm starting with for models::

    class SurveyItem(Item):
        pass


    class SurveyMultiChoice(MultiChoice):
        pass


    class SurveyChoice(Choice):
        votes = models.PositiveIntegerField(default=0)


    class SurveyTrueFalse(TrueFalse):
        true_count = models.PositiveIntegerField(default=0)
        false_count = models.PositiveIntegerField(default=0)


    class SurveyResponse(Response):
        pass

Just before leaving home for South Haven I completed the following:

``python manage.py makemigrations`` -- Got ``No changes detected``

``python manage.py migrate`` -- Got ``No migrations to apply``

This is because I forgot to include ``survey`` in the ``InstalledApps``

Now ``python manage.py makemigrations`` created my five new models.

``python manage.py migrate`` applied survey.0001_initial. I added ``survey.0001_initial`` to git.

I did a commit called "Starting to create the survey app" and pushed my current commits to github.

``python manage.py dumpdata auth.user activity survey polls > 2018-10-19-user-activity-survey-polls.json`` worked.

I copied the resulting file to OneDrive for transfer to the rectory computer.

Finally, I will do another commit and push to save the changes to this file.



