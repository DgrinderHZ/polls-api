from django.utils import timezone
from pollsapp.models import User
from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=150)
    pub_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.question
