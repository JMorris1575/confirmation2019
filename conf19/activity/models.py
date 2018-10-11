from django.db import models
from django.utils.text import Truncator


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


class Item(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    index = models.SmallIntegerField(unique=True)
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.activity.slug + ': ' + str(self.index) + '. ' + str(self.title)

    class Meta:
        ordering = ['index']


class MultiChoice(models.Model):
    text = models.CharField(max_length=512)

    def __str__(self):
        return Truncator(self.text).words(5)

    class Meta:
        verbose_name_plural = 'multiple choice items'


class Choice(models.Model):
    multi_choice = models.ForeignKey(MultiChoice, on_delete=models.CASCADE)
    index = models.SmallIntegerField(unique=True)
    text = models.CharField(max_length=256)
    correct = models.BooleanField(blank=True)

    def __str__(self):
        return self.multi_choice + 'Choice #' + self.index + ' ' + self.text

    class Meta:
        ordering = ['index']
