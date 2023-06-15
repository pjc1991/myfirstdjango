from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question


def question_detail(request, question_id):
    """
    pybo 목록 상세 출력
    """

    q = get_object_or_404(Question, pk=question_id)
    answer_list = q.answer_set.all()
    context = {'question': q, 'answer_list': answer_list}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)

    if not request.method == 'POST':
        form = QuestionForm(instance=question)
        context = {'form': form}
        return render(request, 'pybo/question_form.html', context)

    if request.user != question.author:
        return HttpResponseNotAllowed('잘못된 접근입니다.')

    form = QuestionForm(request.POST, instance=question)

    if not form.is_valid():
        return redirect('pybo:question_detail', question_id=question_id)

    question = form.save(commit=False)
    question.author = request.user
    question.modify_date = timezone.now()
    question.save()

    return redirect('pybo:question_detail', question_id=question_id)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        return HttpResponseNotAllowed('잘못된 접근입니다.')

    question.delete()
    return redirect('pybo:index')
