from django.urls import path

from . import views

urlpatterns = [
    path('', views.questionnaires, name='questionnaires'),
    path('app/', views.ready_questionnaires, name='ready_questionnaires'),
    path('app/start_questionnaire/<int:id>/', views.start_questionnaire, name='start_questionnaire'),
    path('<int:id>/', views.questions, name='questions'),
    path('add_questionnaire/', views.add_questionnaire, name='add_questionnaire'),
    path('add_question/', views.add_question, name='add_question'),
    path('create_questionnaire/', views.create_questionnaire, name='create_questionnaire'),
    path('create_question/', views.create_question, name='create_question'),
    path('delete_questionnaire/', views.delete_questionnaire, name='delete_questionnaire'),
    path('delete_question/', views.delete_question, name='delete_question'),
    path('edit_questionnaire/', views.edit_questionnaire, name='edit_questionnaire'),
    path('edit_question/', views.edit_question, name='edit_question'),
    path('make_edit_questionnaire/', views.make_edit_questionnaire, name='make_edit_questionnaire'),
    path('make_edit_question/', views.make_edit_question, name='make_edit_question'),
]