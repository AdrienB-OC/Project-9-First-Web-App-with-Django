from django.views.generic import ListView, DetailView, TemplateView, \
    FormView, UpdateView, DeleteView
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from itertools import chain
from . import forms, models
from authentication.models import User


@login_required
def home(request):
    user = request.user
    
    tickets = models.Ticket.objects.filter(
        Q(user__in=user.follow.all()) | Q(user=user))

    reviews = models.Review.objects.filter(
        Q(user__in=user.follow.all()) | Q(user=user))

    posts_list = sorted(chain(tickets, reviews),
                        key=lambda x: x.time_created, reverse=True)

    rating_list = [1, 2, 3, 4, 5]
    context = {
        'list': posts_list,
        'rating_list': rating_list,
    }
    return render(request, 'reviews/home.html', context=context)


@login_required
def posts(request):
    user = request.user

    tickets = models.Ticket.objects.filter(user=user)
    print(tickets)
    reviews = models.Review.objects.filter(user=user)
    print(reviews)
    posts_list = sorted(chain(tickets, reviews),
                        key=lambda x: x.time_created, reverse=True)
    context = {
        'list': posts_list,
    }
    return render(request, 'reviews/posts.html', context=context)


@login_required
def ticket_error(request):
    return render(request, 'reviews/ticket_error.html')


@login_required
def write_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'reviews/ticket.html', context={'form': form})


@login_required
def write_review(request, id):
    form = forms.ReviewForm(use_required_attribute=False)
    ticket = models.Ticket.objects.get(id=id)

    # check if ticket already has a review
    if models.Review.objects.filter(ticket=ticket).exists():
        return redirect('ticket_error')

    if request.method == 'POST':
        if id is None:
            return redirect('ticket_error')

        form = forms.ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            rating = form.cleaned_data.get('rating')
            review.rating = rating
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    context = {
        'form': form,
        'ticket': ticket,
    }

    return render(request, 'reviews/ticket_reply.html', context=context)


@login_required
def write_ticket_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            rating = review_form.cleaned_data.get('rating')
            review.rating = rating
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_review.html', context=context)


@login_required
def edit_ticket(request, id):

    ticket = get_object_or_404(models.Ticket, id=id)
    form = forms.TicketForm(instance=ticket)

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, instance=ticket)

        if form.is_valid():
            form.save()

            return redirect('home')

    context = {
        'ticket': ticket,
        'form': form,
    }
    return render(request, 'reviews/edit_ticket.html', context=context)


@login_required
def delete_ticket(request, id):
    ticket = models.Ticket.objects.get(id=id)

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket supprimé avec succès !')
        return redirect('home')

    return render(request, 'reviews/delete_ticket.html', context={'post':
                                                                  ticket})


@login_required
def edit_review(request, id):

    review = get_object_or_404(models.Review, id=id)
    form = forms.ReviewForm(instance=review)

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            review.rating = form.cleaned_data.get('rating')
            review.save()
            return redirect('home')

    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'reviews/edit_review.html', context=context)


@login_required
def delete_review(request, id):
    review = models.Review.objects.get(id=id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Critique supprimée avec succès !')
        return redirect('home')

    return render(request, 'reviews/delete_review.html', context={'post':
                                                                  review})


@login_required
def follow_user(request):
    form = forms.FollowForm()
    user = request.user

    follow_pk = models.UserFollows.objects.all().filter(user=user.pk).values(
        'followed_user')
    follow_list = []
    for f in follow_pk:
        follow_list.append(f['followed_user'])
    follow = User.objects.all().filter(pk__in=follow_list)

    followed_by_pk = models.UserFollows.objects.all().filter(
        followed_user=user.pk).values('user')
    followed_list = []
    for f in followed_by_pk:
        followed_list.append(f['user'])
    followed_by = User.objects.all().filter(pk__in=followed_list)

    if request.method == 'POST':
        print(request.POST)

        # Follow user
        if 'follow' in request.POST:
            form = forms.FollowForm(request.POST)

            if form.is_valid():
                follow_name = form.cleaned_data['follow_user']
                # Check if there is an user with this username
                try:
                    follow_u = User.objects.get(username=follow_name)
                except:
                    follow_u = 'NULL'

                if follow_u != 'NULL':
                    # Make sure current user isn't already following that user
                    try:
                        exists = models.UserFollows.objects.get(
                            user=user, followed_user=follow_u)
                    except:
                        exists = 'NULL'

                    if exists == 'NULL':
                        user_follows = models.UserFollows(
                            user=user, followed_user=follow_u)
                        user_follows.save()
                        user.follow.add(follow_u)
                        messages.success(
                            request, 'Utilisateur suivi avec succès !')

                        return redirect('follow')
                    else:
                        messages.error(
                            request, 'Vous suivez déjà cet utilisateur !')

                        return redirect('follow')

                else:
                    messages.error(request,  "Cet utilisateur n'existe pas !")
                    return redirect('follow')

        # Unfollow user
        elif 'unfollow' in request.POST:
            followed_user = User.objects.get(id=request.POST['unfollow'])
            user.follow.remove(followed_user)
            user_follow = models.UserFollows.objects.filter(
                user=user.pk, followed_user=followed_user.pk)
            user_follow.delete()
            messages.success(request, 'Vous ne suivez plus cet utilisateur !')

            return redirect('follow')

    context = {
        'form': form,
        'follow': follow,
        'followed_by': followed_by,
    }

    return render(request, 'reviews/follow_page.html', context=context)
