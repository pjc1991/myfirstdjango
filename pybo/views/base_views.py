from django.core.paginator import Paginator
from django.shortcuts import render

from pybo.models import Question


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
