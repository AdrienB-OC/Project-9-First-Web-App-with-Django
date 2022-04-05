from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, forms, \
    AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(label="",
                               widget=TextInput(
                                   attrs={'class': 'validate',
                                          'placeholder': 'Email'}))
    password = forms.CharField(label="",
                               widget=PasswordInput(attrs={'placeholder':
                                                           'Mot de Passe'}))
