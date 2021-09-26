from django.test import TestCase
from django.utils import timezone as tz

import datetime as dt

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is in the future.
        """
        time = tz.now() + dt.timedelta(days=30)
        future_question = Question(question_text='Am I recent?', pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is older than 1 day.
        """
        time = tz.now() - dt.timedelta(days=1, seconds=1)
        future_question = Question(question_text='Am I recent?', pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        """
            was_published_recently() returns True for questions whose pub_date
            is within the last day.
        """
        time = tz.now() - dt.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(question_text='Am I recent?', pub_date=time)

        self.assertIs(future_question.was_published_recently(), True)
