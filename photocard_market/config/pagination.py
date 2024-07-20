from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    page_size = 5  # 기본 페이지 크기
    ordering = "create_date"  # 기본 정렬 필드 (내림차순 정렬)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)
