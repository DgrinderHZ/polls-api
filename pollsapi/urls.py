from django.urls import path
from rest_framework.routers import DefaultRouter
from .apiviews import ChoiceList, QuestionList, \
     QuestionDetail, UserCreate, VoteCreate, QuestionChoiceList, PollViewSet


app_name = 'pollsapi'
urlpatterns = [
     path('api/users/', UserCreate.as_view(), name='user_create'),
    path('api/polls/', QuestionList.as_view(), name='pollsapi_list'),
    path('api/polls/<int:pk>/',
         QuestionDetail.as_view(), name='pollsapi_detail'),
    path('api/choices/', ChoiceList.as_view(), name='choicesapi_list'),
    path('api/polls/<int:pk>/choices/<int:choice_pk>/vote/',
                VoteCreate.as_view(), name='voteapi_create'),
    path('api/polls/<int:pk>/choices/',
         QuestionChoiceList.as_view(), name='pollsapi_qstn_choice_list'),
]

# For viewsets
router = DefaultRouter()
router.register('api/pollset', PollViewSet, basename='pollset')
urlpatterns += router.urls
