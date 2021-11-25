from django.db import models

# Create your models here.


class Questionnaires(models.Model):
    name = models.CharField(max_length=10)
    start = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    end = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
    )
    description = models.CharField(max_length=100)


class Questions(models.Model):
    type = models.IntegerField()
    text = models.CharField(max_length=100)
    Questionnaire_id = models.ForeignKey(
        Questionnaires, on_delete=models.CASCADE
    )


class Answers(models.Model):
    text = models.CharField(max_length=100)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)


class Users(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        unique_together = (
            "firstname",
            "lastname",
        )


class UsersAnswers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user = models.CharField(max_length=40)
    answer_id = models.ForeignKey(Answers, on_delete=models.CASCADE)


class UsersFreeAnswers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user = models.CharField(max_length=40)
    answer = models.CharField(max_length=100)
