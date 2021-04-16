from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Create your views here.

def index(request):
    """
    pybo 목록 출력
    """

    question_list = Question.objects.order_by('-created_date')
    context = { 'question_list' : question_list}
    return HttpResponse("Hello, pybo!")
