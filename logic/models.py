from django.db import models

# Create your models here.


class QuestionRecord(models.Model):

    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    base = models.IntegerField(default=0)
