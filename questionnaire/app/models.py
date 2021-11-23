from django.db import models

# Create your models here.


class Questionnaires(models.Model):
    name = models.CharField(max_length=10)
    start = models.DateTimeField(auto_now_add=True, auto_now=False,)
    end = models.DateTimeField(auto_now=False, auto_now_add=False,)
    description = models.CharField(max_length=100)


class Questions(models.Model):
    type = models.IntegerField()
    text = models.CharField(max_length=100)
    Questionnaire_id = models.ForeignKey(Questionnaires, on_delete=models.CASCADE)


class Answers(models.Model):
    text = models.CharField(max_length=100)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
