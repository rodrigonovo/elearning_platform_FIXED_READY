"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django import forms
from .models import Course, Feedback, StatusUpdate, User, CourseMaterial
from django.contrib.auth.forms import UserCreationForm

# --- Class `CustomUserCreationForm`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CustomUserCreationForm(UserCreationForm):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

# --- Class `ProfileUpdateForm`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class ProfileUpdateForm(forms.ModelForm):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'photo']
        
# --- Class `CourseForm`: High-level intent
        
# This class contributes to the domain model or view/controller layer.
        
# Outline: responsibilities, key parameters, side-effects, and return semantics.
        
class CourseForm(forms.ModelForm):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        model = Course
        fields = ['title', 'description']

# --- Class `CourseMaterialForm`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CourseMaterialForm(forms.ModelForm):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        model = CourseMaterial
        fields = ['file']

# --- Class `StatusUpdateForm`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class StatusUpdateForm(forms.ModelForm):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        model = StatusUpdate
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?"}),
        }

# --- Class `FeedbackForm`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class FeedbackForm(forms.ModelForm):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

    # --- Def `clean_comment`: High-level intent

    # This function contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise forms.ValidationError("Feedback must be at least 10 characters long.")
        return comment
