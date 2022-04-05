from django.urls import path
from .views import write_ticket, write_review, write_ticket_review, \
    ticket_error, follow_user, edit_ticket, delete_ticket, edit_review, \
    delete_review, home, posts

urlpatterns = [
    path('write_ticket/', write_ticket, name='write_ticket'),
    path('write_ticket/success/', write_ticket, name='write_ticket_success'),
    path('ticket_reply/<int:id>', write_review, name='ticket_reply'),
    path('write_review/', write_ticket_review, name='post_review'),
    path('error/', ticket_error, name='ticket_error'),
    path('follow/', follow_user, name='follow'),
    path('home/', home, name='home'),
    path('posts/', posts, name='posts'),
    path('edit_ticket/<int:id>', edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:id>', delete_ticket, name='delete_ticket'),
    path('edit_review/<int:id>', edit_review, name='edit_review'),
    path('delete_review/<int:id>', delete_review, name='delete_review')
]
