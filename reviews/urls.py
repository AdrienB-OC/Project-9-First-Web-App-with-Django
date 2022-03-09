from django.urls import path
from .views import write_ticket, write_review, write_ticket_review, \
    ticket_error, follow_user, follow_success, unfollow_user, HomeView

urlpatterns = [
    path('write_ticket/', write_ticket, name='write_ticket'),
    path('write_ticket/success/', write_ticket, name='write_ticket_success'),
    path('ticket_reply/<int:id>', write_review, name='ticket_reply'),
    path('write_review/', write_ticket_review, name='post_review'),
    path('error/', ticket_error, name='ticket_error'),
    path('follow/', follow_user, name='follow'),
    path('follow_success/', follow_success, name='follow_success'),
    path('unfollow/<int:id>', unfollow_user, name='unfollow'),
    path('home/', HomeView.as_view(), name='home'),
]