from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from pybo.models import Question, Board
from django.utils import timezone
from .forms import QuestionForm

# Create your views here.


def index(request):
    """
    pybo 목록 출력
    """

    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 목록 상세 출력
    """

    q = get_object_or_404(Question, pk=question_id)
    answer_list = q.answer_set.all()
    context = {'question': q, 'answer_list': answer_list}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'pybo/question_form.html', context)


def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get(
        'content'), create_date=timezone.now())

    return redirect('pybo:detail', question_id=question_id)


def board_list(request):
    """
    pybo 게시판 목록 출력
    """

    board_item_list = Board.objects.order_by('-create_date')
    context = {'board_list': board_item_list}
    return render(request, 'pybo/board_list.html', context)


def board_detail(request, board_id):
    """
    pybo 게시판 상세 출력
    """

    board_detail_item = get_object_or_404(Board, pk=board_id)
    comment_list = board_detail_item.comment_set.all()
    context = {'board': board_detail_item, 'comment_list': comment_list}
    return render(request, 'pybo/board_detail.html', context)
