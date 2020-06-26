from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['score', 'summary', 'body']
		widgets = {
			'score': forms.NumberInput(
				attrs = {
					'class': 'form-control',
					'min': 0,
					'max': 10
					}
				),
			'summary': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'rows': 2
					}
				),
			'body': forms.Textarea(attrs = {'class': 'form-control'})
			}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']
		widgets = {
			'body': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'rows': 2
					}
				)
			}
