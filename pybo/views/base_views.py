from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from pybo.models import Question


def index(request):
    """
    pybo 목록 출력
    """

    page = request.GET.get('page', '1')  # 페이지
    keyword = request.GET.get('keyword', None)  # 검색어

    question_list = Question.objects.order_by('-create_date')

    if not page.isdecimal():
        page = 1

    if keyword:
        question_list = question_list.filter(
            Q(subject__icontains=keyword) |  # 제목
            Q(content__icontains=keyword) |  # 내용
            Q(author__username__icontains=keyword) |  # 질문자
            Q(answer__content__icontains=keyword) |  # 답변 내용
            Q(answer__author__username__icontains=keyword)  # 답변자
        ).distinct()

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    page_obj.elided_page_range = paginator.get_elided_page_range(page)

    context = {
        'question_list': page_obj
        , 'query_dict': request.GET
    }

    return render(request, 'pybo/question_list.html', context)
