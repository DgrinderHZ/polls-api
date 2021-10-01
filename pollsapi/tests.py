from pollsapp.models import User
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from . import apiviews


class TestPoll(APITestCase):
    def setUp(self) -> None:
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.factory = APIRequestFactory()
        self.view = apiviews.PollViewSet.as_view({'get': 'list'})
        self.uri = '/api/pollset/'

    @staticmethod
    def setup_user():
        return User.objects.create(
            username='test',
            email='test@test.test',
            password='test'
        )

    def test_list(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
         )
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code, 200,
            f'Expected Response Code 200, \
                received {response.status_code} instead.'
        )


class TestPoll2(APITestCase):
    @staticmethod
    def setup_user():
        return User.objects.create(
            username='test',
            email='test@test.test',
            password='test'
        )

    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.uri = '/api/pollset/'
        self.client = APIClient()

    def test_list2(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(username="test", password="test")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(username="test", password="test")
        params = {
            "question": "How are you?",
            "created_by": 1,
            }
        response = self.client.post(self.uri, params, format='json')
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
