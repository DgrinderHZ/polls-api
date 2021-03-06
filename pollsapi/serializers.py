from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer


from pollsapp.models import Question, Choice, User, Vote
from .models import Poll


class PollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class ChoiceSerializer(ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
