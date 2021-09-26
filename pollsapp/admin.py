from .models import Choice, Question
from django.contrib import admin


class QuestionModel(admin.ModelAdmin):
    fields = ['question_text', 'pub_date']


class ChoiceModel(admin.ModelAdmin):
    fieldsets = [
        ('Choice information', {'fields': ['choice_text', 'votes']}),
        ('Question information', {'fields': ['question']}),
    ]


admin.site.register(Question, QuestionModel)
admin.site.register(Choice, ChoiceModel)
