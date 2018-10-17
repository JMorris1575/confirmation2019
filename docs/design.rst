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

