from django.urls import path
from .views import detail, index, results, vote


app_name='polls'
urlpatterns = [
    path('polls/', index, name='index'),
    path('polls/<int:question_id>/', detail, name='detail'),
    path('polls/<int:question_id>/results/', results, name='results'),
    path('polls/<int:question_id>/vote/', vote, name='vote'),

]
