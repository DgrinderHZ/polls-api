from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=150)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.question
