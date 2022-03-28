from django import forms
from django.forms.widgets import TextInput
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(label="Note", required=True,
                               choices=RATING_CHOICES,
                               widget=forms.RadioSelect)

    class Meta:
        model = models.Review
        fields = ['headline', 'body']

    field_order = ['headline', 'rating', 'body']


class FollowForm(forms.ModelForm):
    follow_user = forms.CharField(
        label="", widget=TextInput(attrs={'placeholder': "Nom d'utilisateur"}))

    class Meta:
        model = models.UserFollows
        fields = []
