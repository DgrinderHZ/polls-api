from django.urls import path
from .apiviews import ChoiceList, QuestionList, \
     QuestionDetail, VoteCreate, QuestionChoiceList


app_name = 'pollsapi'
urlpatterns = [
    path('api/polls/', QuestionList.as_view(), name='pollsapi_list'),
    path('api/polls/<int:pk>/',
         QuestionDetail.as_view(), name='pollsapi_detail'),
    path('api/choices/', ChoiceList.as_view(), name='choicesapi_list'),
    path('api/polls/<int:pk>/choices/<int:choice_pk>/vote/', VoteCreate.as_view(), name='voteapi_create'),
    path('api/polls/<int:pk>/choices/',
         QuestionChoiceList.as_view(), name='pollsapi_qstn_choice_list'),
]
