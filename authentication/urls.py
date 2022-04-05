from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup_page
from .forms import CustomAuthForm

urlpatterns = [
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True, authentication_form=CustomAuthForm),
     name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup_page, name='signup')
]
