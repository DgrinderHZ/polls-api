from django.urls import path
from rest_framework.routers import DefaultRouter
from .apiviews import ChoiceList, QuestionList, \
     QuestionDetail, UserCreate, UserLoginView, \
     VoteCreate, QuestionChoiceList, PollViewSet
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView


schema_view = get_swagger_view(title='Polls API')

app_name = 'pollsapi'
urlpatterns = [
     path('api/users/', UserCreate.as_view(), name='user_create'),
     path('api/login/', UserLoginView.as_view(), name='user_login'),
     path('api/polls/', QuestionList.as_view(), name='pollsapi_list'),
     path('api/polls/<int:pk>/',
          QuestionDetail.as_view(), name='pollsapi_detail'),
     path('api/choices/', ChoiceList.as_view(), name='choicesapi_list'),
     path(
          'api/polls/<int:pk>/choices/<int:choice_pk>/vote/',
          VoteCreate.as_view(), name='voteapi_create'
     ),
     path('api/polls/<int:pk>/choices/',
          QuestionChoiceList.as_view(), name='pollsapi_qstn_choice_list'),
     path(r'api/docs/', schema_view),
]

# For viewsets
router = DefaultRouter()
router.register('api/pollset', PollViewSet, basename='pollset')
urlpatterns += router.urls
