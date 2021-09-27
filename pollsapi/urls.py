from django.urls import path
from .apiviews import QuestionList, QuestionDetail


app_name = 'pollsapi'
urlpatterns = [
    path('api/polls/', QuestionList.as_view(), name='polls_list'),
    path('api/polls/<int:pk>/',
         QuestionDetail.as_view(), name='polls_detail'),
]
