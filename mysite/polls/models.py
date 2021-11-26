import datetime

from django.db import models
from django.utils import timezone

# each model represented by a class that subclasses djgano.db.models.Model
# each field is represented by an instance of a Field class so Django knows what type of data each field holds
class Question(models.Model):
    # CharField requires max_length argument
    question_text = models.CharField(max_length=200)
    # optional first opositional argument to a Field designates a human-readable name
    pub_date = models.DateTimeField('date published')
    # this allows a string to be returned when we query all of the objects in the Question model
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text