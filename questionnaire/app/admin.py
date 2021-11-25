from django.contrib import admin
from .models import (
    Questionnaires,
    Questions,
    Answers,
    Users,
    UsersAnswers,
    UsersFreeAnswers,
)


# Register your models here.
admin.site.register(Questionnaires)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Users)
admin.site.register(UsersAnswers)
admin.site.register(UsersFreeAnswers)
