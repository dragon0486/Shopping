from rest_framework.pagination import PageNumberPagination

class CoursePageNumberPagination(PageNumberPagination):
    """课程列表数据的分页器"""
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 2
    max_page_size = 10