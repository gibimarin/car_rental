from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'subject', 'message']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a brief subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Please describe your issue or feedback in detail.'}),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '')
        if len(subject.strip()) < 3:
            raise forms.ValidationError('Subject must be at least 3 characters long.')
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message.strip()) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message
    
    from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_id', 'car_name', 'car_desc', 'price', 'image']
        widgets = {
            'car_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'car_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'car_id': 'Car ID (Unique Identifier)',
            'car_name': 'Car Name',
            'car_desc': 'Description',
            'price': 'Price per Day (Rs)',
            'image': 'Vehicle Image'
        }
