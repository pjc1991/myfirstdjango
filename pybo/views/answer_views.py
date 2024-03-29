from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404, render, resolve_url
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pybo.forms import AnswerForm
from pybo.models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """

    if not request.method == 'POST':
        return redirect('pybo:question_detail', question_id=question_id)

    form = AnswerForm(request.POST)
    form.user = request.user
    form.create_date = timezone.now()

    if not form.is_valid():
        return redirect('pybo:question_detail', question_id=question_id)

    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(
        author=request.user,
        content=form.cleaned_data['content'],
        create_date=timezone.now(),
    )

    return redirect(get_answer_uri(question_id, question.answer_set.last().id))


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
        return redirect('pybo:question_detail', question_id=answer.question.id)

    answer = form.save(commit=False)
    answer.author = request.user
    answer.modify_date = timezone.now()
    answer.save()

    return redirect(get_answer_uri(answer.question.id, answer.id))


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        return HttpResponseNotAllowed('잘못된 접근입니다.')

    answer.delete()
    return redirect('pybo:question_detail', question_id=answer.question.id)


@api_view(['POST'])
def answer_vote_api(request, answer_id):
    """
    pybo 답변 추천
    """
    answer = get_object_or_404(Answer, pk=answer_id)

    if not request.user.is_authenticated:
        return Response({'error': '로그인을 해주세요.'}, status=401)

    if request.user == answer.author:
        return Response({'error': '자신이 작성한 글은 추천할 수 없습니다.'}, status=400)

    if answer.voter.filter(pk=request.user.pk).exists():
        answer.voter.remove(request.user)
        return Response({'vote_count': answer.voter.count(), 'message': '추천 취소'}, status=201)

    answer.voter.add(request.user)
    return Response({'vote_count': answer.voter.count(), 'message': '추천 완료'}, status=201)


'''
Utility functions here
'''


def get_answer_uri(question_id: int, answer_id: int):
    """
    uri for answer_n
    """
    return '{}#answer_{}'.format(resolve_url('pybo:question_detail', question_id=question_id), str(answer_id))
