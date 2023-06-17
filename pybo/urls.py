from django.urls import path, include
from rest_framework import routers

import pybo.views.answer_views
import pybo.views.base_views
import pybo.views.question_views

app_name = 'pybo'


urlpatterns = [
    path('', pybo.views.base_views.index, name='index'),
    path('<int:question_id>/', pybo.views.question_views.question_detail, name='question_detail'),
    path('question/create/', pybo.views.question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', pybo.views.question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', pybo.views.question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', pybo.views.question_views.question_vote_api, name='question_vote'),
    path('answer/create/<int:question_id>/', pybo.views.answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', pybo.views.answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', pybo.views.answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', pybo.views.answer_views.answer_vote_api, name='answer_vote'),
]
