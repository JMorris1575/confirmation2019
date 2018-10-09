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

