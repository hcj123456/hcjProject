from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):
    page_size = 4
    page_query_param = 'p'
    page_size_query_param = 's'
    max_page_size = 20
    invalid_page_message = '页码无效'