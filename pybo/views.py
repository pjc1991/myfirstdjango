from django.shortcuts import redirect, render, get_object_or_404
from pybo.models import Question
from django.utils import timezone
from .forms import QuestionForm
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    """
    pybo 목록 출력
    """
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    page_obj.elided_page_range = paginator.get_elided_page_range(page)
    context = {'question_list': page_obj}
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
