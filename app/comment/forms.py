from django import forms
from app.comment.models import CommentModel








class StarRatingRadioSelect(forms.RadioSelect):
    template_name = 'widgets/star_rating_widget.html'


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['stars', 'content', 'image']
        widgets = {
            'stars': StarRatingRadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'content': forms.Textarea(attrs={
                'class': 'custom-content-class',
                'placeholder': 'Enter your comment here...',
                'rows': 2,
                'cols': 70,
            }),
        }
