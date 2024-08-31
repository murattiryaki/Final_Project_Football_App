from django import forms
from .models import StadiumReview

class StadiumReviewForm(forms.ModelForm):
    class Meta:
        model = StadiumReview
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'Rate 1-5'}),
        }
