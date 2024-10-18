from django import forms
from django.forms import modelformset_factory
from .models import Project,Tag,Review

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'title', 'team_members', 'faculty_members', 'department', 
            'university', 'description', 'video', 'document','image','tags'
        ]

        tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),  # 1-5 star rating
        }