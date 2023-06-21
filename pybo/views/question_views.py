from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pybo.forms import QuestionForm
from pybo.models import Question


def question_detail(request, question_id):
    """
    pybo 목록 상세 출력
    """

    q = get_object_or_404(Question, pk=question_id)
    # order by voter count
    answer_list = q.answer_set.annotate(voter_count=Count('voter')).order_by('-voter_count', '-create_date')
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


@api_view(['POST'])
def question_vote_api(request, question_id):
    """
    pybo 질문 추천
    """
    question = get_object_or_404(Question, pk=question_id)

    if not request.user.is_authenticated:
        return Response({'error': '로그인을 해주세요.'}, status=401)

    if request.user == question.author:
        return Response({'error': '자신이 작성한 글은 추천할 수 없습니다.'}, status=403)

    if question.voter.filter(pk=request.user.pk).exists():  # 추천 취소
        question.voter.remove(request.user)
        return Response({'vote_count': question.voter.count(), 'message': '추천 취소'}, status=201)

    question.voter.add(request.user)
    return Response({'vote_count': question.voter.count(), 'message': '추천 완료'}, status=201)
