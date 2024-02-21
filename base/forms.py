from django.forms import ModelForm
from .models import Room, Question,Solution


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # ['name', 'description']  # '__all__'


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'  # ['name', 'description']  # '__all__'

class SolutionForm(ModelForm):
    class Meta:
        model = Solution
        fields = '__all__'  # ['name', 'description']  # '__all__'
