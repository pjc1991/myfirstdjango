from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone

from pybo.forms import AnswerForm
from pybo.models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """

    if not request.method == 'POST':
        return redirect('pybo:detail', question_id=question_id)

    form = AnswerForm(request.POST)
    form.user = request.user
    form.create_date = timezone.now()

    if not form.is_valid():
        return redirect('pybo:detail', question_id=question_id)

    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(
        author=request.user,
        content=form.cleaned_data['content'],
        create_date=timezone.now(),
    )

    return redirect('pybo:detail', question_id=question_id)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if not request.method == 'POST':
        form = AnswerForm(instance=answer)
        context = {'form': form}
        return render(request, 'pybo/question_modify.html', context)

    if request.user != answer.author:
        return HttpResponseNotAllowed('잘못된 접근입니다.')

    form = AnswerForm(request.POST, instance=answer)

    if not form.is_valid():
        return redirect('pybo:detail', question_id=answer.question.id)

    answer = form.save(commit=False)
    answer.author = request.user
    answer.modify_date = timezone.now()
    answer.save()

    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        return HttpResponseNotAllowed('잘못된 접근입니다.')

    answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
