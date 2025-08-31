# core/forms.py

from django import forms
from .models import Course, Feedback, StatusUpdate, User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users, extending Django's UserCreationForm
    to include the custom 'role' field and other user information.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

class CourseForm(forms.ModelForm):
    """
    A form for creating and updating Course instances.
    """
    class Meta:
        model = Course
        fields = ['title', 'description', 'course_material']

class StatusUpdateForm(forms.ModelForm):
    """
    A form for creating StatusUpdate instances.
    """
    class Meta:
        model = StatusUpdate
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?"}),
        }

class FeedbackForm(forms.ModelForm):
    """
    A form for creating and updating Feedback instances.
    Includes custom validation for the 'comment' field.
    """
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

    def clean_comment(self):
        """
        Custom validation to ensure the feedback comment is at least 10 characters long.
        """
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise forms.ValidationError("Feedback must be at least 10 characters long.")
        return comment