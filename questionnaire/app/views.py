from django.shortcuts import render, redirect
from .models import (
    Questionnaires,
    Questions,
    Answers,
    Users,
    UsersAnswers,
    UsersFreeAnswers,
)
from datetime import datetime


def questionnaires(request):
    questionnaires = Questionnaires.objects.all()
    context = {"elements": questionnaires}
    return render(request, "main.html", context)


def ready_questionnaires(request):
    questionnaires = Questionnaires.objects.filter(end__gte=datetime.now())
    context = {"elements": questionnaires}
    name = request.COOKIES.get("firstname")
    if name is not None:
        print("Name:", name)
    return render(request, "ready_main.html", context)


def start_questionnaire(request, id=None):
    context = {}
    if request.COOKIES.get("firstname") is None:
        return render(request, "need_to_login.html", context)
    if id is None:
        return redirect("ready_questionnaires")
    questions = Questions.objects.filter(Questionnaire_id=id)
    context = {"questions": questions, "questionnaire_id": id, "answers": {}}
    for question in questions:
        answers = Answers.objects.filter(question_id=question)
        context["answers"][f"answers_{question.id}"] = answers
    return render(request, "ready_questions.html", context)


def questions(request, id=None):
    context = {}
    if id is None:
        return render(request, "main.html", context)
    questions = Questions.objects.filter(Questionnaire_id=id)
    context = {"questions": questions, "questionnaire_id": id}
    return render(request, "questions.html", context)


def register(request):
    context = {}
    return render(request, "register.html", context)


def login(request):
    context = {"message": "Logining..."}
    return render(request, "custom_login.html", context)


def save_results(request):
    data = dict(request.GET)
    if "anonymous" in data:
        user = request.COOKIES.get("id")
    else:
        user = (
            request.COOKIES.get("firstname")
            + " "
            + request.COOKIES.get("lastname")
        )
    for key in data:
        if key.isnumeric():
            question = Questions.objects.filter(id=int(key)).first()
            if question.type != 1:
                answer = Answers.objects.filter(id=int(data[key][0])).first()
                user_answer = UsersAnswers(
                    question_id=question, user=user, answer_id=answer
                )
            else:
                answer = data[key][0]
                user_answer = UsersFreeAnswers(
                    question_id=question, user=user, answer=answer
                )
            user_answer.save()
    return redirect("ready_questionnaires")


def make_login(request):
    data = dict(request.GET)
    user = Users.objects.filter(
        firstname=data["firstname"][0],
        lastname=data["lastname"][0],
    ).first()
    if user is None:
        return render(
            request,
            "custom_login.html",
            {"message": "User not founded. Try again..."},
        )
    if user.password == data["password"][0]:
        response = redirect("ready_questionnaires")
        response.set_cookie("id", user.id, max_age=None)
        response.set_cookie("firstname", user.firstname, max_age=None)
        response.set_cookie("lastname", user.lastname, max_age=None)
        return response
    else:
        return render(
            request,
            "custom_login.html",
            {"message": "Wrong Password. Try again..."},
        )


def make_register(request):
    data = dict(request.GET)
    user = Users(
        firstname=data["firstname"][0],
        lastname=data["lastname"][0],
        password=data["password"][0],
    )
    user.save()
    return make_login(request)


def edit_questionnaire(request):
    id = request.GET.get("id")
    context = {}
    if id is not None:
        item = Questionnaires.objects.filter(id=id).first()
        context = {
            "name": item.name,
            "description": item.description,
            "end": item.end.strftime("%Y-%m-%d"),
            "id": id,
        }
    return render(request, "edit_form_questionnaire.html", context)


def edit_question(request):
    id = request.GET.get("id")
    questionnaire_id = request.GET.get("questionnaire_id")
    context = {}
    if id is not None:
        item = Questions.objects.filter(id=id).first()
        answers = Answers.objects.filter(question_id=item)
        context = {
            "type": item.type,
            "text": item.text,
            "id": id,
            "questionnaire_id": questionnaire_id,
            "answers": answers,
        }
    return render(request, "edit_form_question.html", context)


def make_edit_questionnaire(request):
    id = request.GET.get("id")
    item = Questionnaires.objects.filter(id=id).first()
    item.name = request.GET.get("name")
    item.description = request.GET.get("description")
    item.end = request.GET.get("end")
    item.save()
    return redirect("questionnaires")


def make_edit_question(request):
    questionnaire_id = request.GET.get("questionnaire_id")
    id = request.GET.get("question_id")
    data = dict(request.GET)
    item = Questions.objects.filter(id=id).first()
    item.type = request.GET.get("type")
    item.text = request.GET.get("text")
    item.save()
    Answers.objects.filter(question_id=item).delete()
    for key in data:
        if "answer" == key[:6].lower():
            answer = Answers(text=data[key][0], question_id=item)
            answer.save()
    return redirect("questions", questionnaire_id)


def add_questionnaire(request):
    context = {}
    return render(request, "add_form_questionnaire.html", context)


def add_question(request):
    name = "questionnaire_id"
    questionnaire_id = request.GET.get(name)
    context = {name: questionnaire_id}
    return render(request, "add_form_question.html", context)


def delete_questionnaire(request):
    id = request.GET.get("id")
    if id is not None:
        Questionnaires.objects.filter(id=id).delete()
    return redirect("questionnaires")


def delete_question(request):
    id = request.GET.get("id")
    questionnaire_id = request.GET.get("questionnaire_id")
    if id is not None:
        Questions.objects.filter(id=id).delete()
    return redirect("questions", questionnaire_id)


def create_questionnaire(request):
    data = dict(request.GET)
    new_questionnaire = Questionnaires(
        name=data["name"][0],
        end=data["end"][0],
        description=data["description"][0],
    )
    new_questionnaire.save()
    return redirect("questionnaires")


def create_question(request):
    data = dict(request.GET)
    id = data["questionnaire_id"][0]
    questionnaire = Questionnaires.objects.filter(id=id).first()
    new_question = Questions(
        type=data["type"][0],
        text=data["text"][0],
        Questionnaire_id=questionnaire,
    )
    new_question.save()
    for key in data:
        if "answer" == key[:6].lower():
            answer = Answers(text=data[key], question_id=new_question)
            answer.save()
    return redirect("questions", id)
