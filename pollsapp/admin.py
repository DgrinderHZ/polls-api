from .models import Choice, Question
from django.contrib import admin

# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_text', 'pub_date']
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
