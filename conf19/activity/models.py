from django.db import models
from django.conf import settings
from django.utils.text import Truncator

from heapq import merge


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


# +-----------------------------+
# |                             |
# | Prerequisite Models Section |
# |                             |
# +-----------------------------+


class Image(models.Model):
    filename = models.CharField(max_length=30)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.filename


class Activity(models.Model):
    index = models.SmallIntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)
    overview = models.CharField(max_length=512, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    publish_date = models.DateField(null=True)
    closing_date = models.DateField(null=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['index']
        verbose_name_plural = 'activities'


# +------------------------------+
# |                              |
# | Abstract Base Models Section |
# |                              |
# +------------------------------+


class Item(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    index = models.SmallIntegerField()
    title = models.CharField(max_length=25, null=True, blank=True)
    item_type = models.CharField(max_length=2,  # indicates the type of this item
                                 choices=[('AC', 'action'),     # item belongs to the action app
                                          ('DI', 'discuss'),    # Item belongs to the discussion app
                                          ('SU', 'survey')],    # Item belongs to the survey app
                                 default = 'AC')
    privacy_type = models.CharField(max_length=2,   # indicates privacy level of an item
                                 choices=[('OP', 'Open'),               # responder able to be openly published
                                          ('SA', 'Semi-Anonymous'),     # responder only visible to team members
                                          ('AN', 'Anonymous')],         # responder not saved
                                 default='OP')

    def __str__(self):
        return self.activity.slug + '/' + self.get_item_type_display() + '/' + str(self.index)

    class Meta:
        ordering = ['index']
        abstract = True
        unique_together = ('activity', 'index')

    def previous(self):
        """
        Returns the previous page if there is one, otherwise returns None
        :return: '/activity/<activity_slug>/<item_type>/<item_index>/ or None
        """
        index = self.index
        slug = self.activity.slug
        item_type = self.get_item_type_display()
        if index == 1:
            return None
        else:
            return '/activity/' + slug + '/' + item_type + '/' + str(index - 1) + '/'

    def next(self):
        """
        Returns the next item if there is one, otherwise returns None
        :return: '/activity/<activity_slug>/<item_type>/<page_index>/ or None
        """
        index = self.index
        slug = self.activity.slug
        item_type = self.get_item_type_display()
        max = len(Item.objects.filter(activity=self.activity))
        if index == max:
            return None
        else:
            return '/activity/' + slug + '/' + item_type + '/' + str(index + 1) + '/'


class MultiChoice(Item):
    text = models.CharField(max_length=512)

    def __str__(self):
        return Truncator(self.text).words(5)

    class Meta(Item.Meta):
        ordering = ['index']


    def get_text(self):
        return self.text

    def get_choices(self):
        return self.choice_set

    def get_subtext(self):
        choices = self.get_choices
        subtext = []
        for choice in choices:
            subtext.append(choice.text)
        return subtext


class Choice(models.Model):
    multi_choice = models.ForeignKey(MultiChoice, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    correct = models.BooleanField(blank=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['pk']


class TrueFalse(Item):
    statement = models.CharField(max_length=512)
    correct_answer = models.BooleanField(null=True, blank=True)
    true_count = models.PositiveIntegerField(default=0)
    false_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.statement

    class Meta(Item.Meta):
        ordering = ['index']

    def get_text(self):
        return self.statement

    def get_subtext(self):
        return ['True or False']


class Response(models.Model):
    """
    Records the user's responses for the various kinds of items and keeps track of which items have been completed.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # could be 'Unidentified'
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    index = models.SmallIntegerField()      # indicates which item in the activity received this response
    multi_choice = models.PositiveSmallIntegerField(null=True, blank=True)
    true_false = models.BooleanField(default=False)
    correct = models.NullBooleanField(null=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        if name[-1] == 's':
            possessive_ending = "'"
        else:
            possessive_ending = "'s"
        return name + possessive_ending + ' response to ' + self.activity.slug + '/' + str(self.index)

    def is_correct(self):
        return self.correct

    # def can_delete(self):
    #     """
    #     Returns True if this response can be deleted, false otherwise
    #     A response can be deleted if it's answer has not been revealed and if the user has not completed any pages
    #     beyond this one in the current activity
    #     :return: boolean
    #     """
    #     this_index = self.page.index
    #     number_completed = len(Response.objects.filter(user=self.user, activity=self.activity))
    #     if (this_index == number_completed) and not self.page.reveal_answer:
    #         return True
    #     else:
    #         return False

    def can_goto_next(self):
        """
        Returns true if this user has completed this page and so can go to the next
        :return: boolean
        """
        return self.completed


class Completed(models.Model):
    """
    Records whether the user has responded to a particular item
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    index = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.activity) + ' ' + str(self.index) + " completed by: " + self.user.first_name + ' ' + self.user.last_name
