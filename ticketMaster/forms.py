from django import forms
from .models import Event, Comment, SavedEvent


# Define a form class for the Event model
class EventForm(forms.ModelForm):
    class Meta:
        # Specify the model associated with this form
        model = Event
        fields = '__all__'


# Define a form class for the Comment model
class CommentForm(forms.ModelForm):
    class Meta:
        # Specify the model associated with this form
        model = Comment
        fields = ['starRating', 'comment']


# Define a form class for the SavedEvent model
class SavedEventForm(forms.ModelForm):
    class Meta:
        # Specify the model associated with this form
        model = SavedEvent
        fields = '__all__'
