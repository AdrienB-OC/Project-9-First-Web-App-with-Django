from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain
from . import forms, models
from authentication.models import User


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    context = {
        'posts': tickets,
        'reviews': reviews,
    }
    return render(request, 'reviews/home.html', context=context)


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'reviews/home.html'
    context_object_name = 'posts_lists'
    model = models.Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        tickets = models.Ticket.objects.filter()
        reviews = models.Review.objects.filter()
        posts_list = sorted(chain(tickets, reviews),
                            key=lambda x: x.time_created, reverse=True)
        context.update({
            'list': posts_list,
        })
        return context


class HomeView2(LoginRequiredMixin, ListView):
    template_name = 'reviews/home.html'
    model = models.Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeView2, self).get_context_data(**kwargs)
        context['tickets'] = models.Ticket.objects.all()
        context['reviews'] = models.Review.objects.all()
        return context


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


class WriteTicketView(LoginRequiredMixin, FormView):
    template_name = 'reviews/ticket.html'
    form_class = forms.TicketForm

    success_url = ''


@login_required
def write_review(request, id):
    form = forms.ReviewForm()
    ticket = models.Ticket.objects.get(id=id)

    if request.method == 'POST':
        if id is None:
            return redirect('ticket_error')

        form = forms.ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    context = {
        'form': form,
        'ticket': ticket,
    }

    return render(request, 'reviews/ticket_reply.html', context=context)


class WriteReview(LoginRequiredMixin, DetailView):
    template_name = 'reviews/ticket_reply.html'
    model = models.Ticket

    def get_context_data(self, **kwargs):
        context = super(WriteReview, self).get_context_data(**kwargs)
        review_form = forms.ReviewForm()
        context.update({
            'review_form': review_form,
        })
        return context

    def form_valid(self, form):
        form.save(commit=False)
        t_id = self.kwargs[id]
        form.ticket = models.Ticket.objects.get(id=t_id)
        form.save()
        return super(WriteReview, self).form_valid(form)

    def post(self, request, **kwargs):
        context = super(WriteReview, self).get_context_data(**kwargs)
        review_form = forms.ReviewForm()
        context.update({
            'review_form': review_form,
        })
        return HttpResponseRedirect(reverse('ticket_reply'))


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
def follow_user(request):
    if 'search' in request.POST:
        f_user = request.POST['search']
        print(f_user)
        user = request.user
        user.following.add(f_user)
        user_follow = models.UserFollows.objects.create(user=user.pk,
                                                        follow_user=f_user.pk)
        user_follow.save()
        return redirect('reviews/follow_success.html')

    return render(request, 'reviews/follow_page.html')


@login_required
def follow_success(request):
    context = {}
    if request == 'POST':
        user = User.objects.get(username='search')
        context.update({
            'user_followed': user,
        })

    return render(request, 'reviews/follow_success.html',
                  context=context)


class Follow(LoginRequiredMixin, ListView):
    pass
