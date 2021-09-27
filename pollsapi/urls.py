from django.urls import path
from .apiviews import ChoiceList, QuestionList, QuestionDetail, VoteCreate


app_name = 'pollsapi'
urlpatterns = [
    path('api/polls/', QuestionList.as_view(), name='pollsapi_list'),
    path('api/polls/<int:pk>/',
         QuestionDetail.as_view(), name='pollsapi_detail'),
    path('api/choices/', ChoiceList.as_view(), name='choicesapi_list'),
    path('api/vote/', VoteCreate.as_view(), name='voteapi_create'),
]
