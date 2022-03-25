from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('question/create/', views.question_create, name='question_create'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('board/', views.board, name='board'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/create/', views.board_create, name='board_create'),
]