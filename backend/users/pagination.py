from rest_framework.pagination import PageNumberPagination


class BackendPagination(PageNumberPagination):
    page_size_query_param = 'limit'
