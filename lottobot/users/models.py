from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    # 그룹 및 권한 필드의 related_name 수정
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # 충돌 방지
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # 충돌 방지
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )