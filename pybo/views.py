from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pybo.models import Question

# Create your views here.

def index(request):
    """
    pybo 목록 출력
    """

    question_list = Question.objects.order_by('-created_date')
    context = { 'question_list' : question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 목록 상세 출력
    """

    q = get_object_or_404(Question, pk=question_id)
    context = { 'question': q }
    return render(request, 'pybo/question_detail.html', context)
