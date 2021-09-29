from django.test import TestCase
from django.utils import timezone as tz
from django.urls import reverse

import datetime as dt

from .models import Question, User


def create_user():
    user = User.objects.create(
            username='test',
            email='test@test.test',
            password='test'
        )
    return user


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is in the future.
        """
        time = tz.now() + dt.timedelta(days=30)
        future_question = Question(
            question_text='Am I recent?',
            pub_date=time,
            created_by=create_user()
        )

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is older than 1 day.
        """
        time = tz.now() - dt.timedelta(days=1, seconds=1)
        future_question = Question(
            question_text='Am I recent?',
            pub_date=time,
            created_by=create_user())

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
            was_published_recently() returns True for questions whose pub_date
            is within the last day.
        """
        time = tz.now() - dt.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(
            question_text='Am I recent?',
            pub_date=time,
            created_by=create_user())

        self.assertIs(future_question.was_published_recently(), True)


def create_question(question_text, days, user):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = tz.now() + dt.timedelta(days=days)
    return Question.objects.create(
        question_text=question_text,
        pub_date=time,
        created_by=user)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        user = create_user()
        question = create_question(question_text="Past question.", days=-30, user=user)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        user = create_user()
        create_question(question_text="Future question.", days=30, user=user)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        user = create_user()
        question = create_question(
            question_text="Past question.",
            days=-30,
            user=user)
        create_question(question_text="Future question.", days=30, user=user)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        user = create_user()
        question1 = create_question(question_text="Past question 1.", days=-30, user=user)
        question2 = create_question(question_text="Past question 2.", days=-5, user=user)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetaillViewtests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        user = create_user()
        future_question = create_question('Future Question?', 5, user=user)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        user = create_user()
        past_question = create_question('Past Question.', -5, user=user)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResulsViewTests(TestCase):
    def test_future_question(self):
        user = create_user()
        future_question = create_question('Future Question', 20, user=user)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        user = create_user()
        past_question = create_question('Past Question', days=-20, user=user)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
