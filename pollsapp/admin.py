from .models import Choice, Question, Vote
from django.contrib import admin

# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_text', 'pub_date', 'created_by']
    inlines = [ChoiceInline]
    list_display = (
        'question_text', 'pub_date', 'was_published_recently', 'created_by'
    )
    list_filter = ['pub_date']
    search_fields = ['question_text']


class VoteAdmin(admin.ModelAdmin):
    fields = ['question', 'choice', 'voted_by']
    list_display = ['question', 'choice', 'voted_by']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote, VoteAdmin)
