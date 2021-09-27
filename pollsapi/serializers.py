from rest_framework.serializers import ModelSerializer


from pollsapp.models import Question, Choice, Vote


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
