from django.db import models


class State(models.TextChoices):
    END = "E", "판매완료"
    BEGIN = "B", "판매중"
    START = "S", "등록"
