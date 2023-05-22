from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book, CONDITION
from django.db.models import Q
from .forms import BookForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404


# Create your views here.
def page_not_found_view(request):
    return render(request, '404.html', status=404)


class HomeView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/home.html'
    paginate_by = 7
    context_object_name = 'books_list'

    def get_queryset(self):
        filter_params = self.request.GET.get('filter')  # region,education
        self.wished_books = Book.objects.filter(owner=self.request.user, status='W', active=True)
        offered_books = Book.objects.filter(status='O', active=True).select_related('owner')

        try:
            if filter_params == 'country':
                offered_books = offered_books.filter(owner__country=self.request.user.country)
            elif filter_params == 'region':
                offered_books = offered_books.filter(owner__region=self.request.user.region)
            elif filter_params == 'education':
                offered_books = offered_books.filter(owner__education__trigram_similar=self.request.user.education)
        except ValueError:
            pass

        titles_list = list(self.wished_books.values_list('title', flat=True))
        queries = [Q(title__trigram_similar=title) for title in titles_list]  # create a list of Q objects
        combined_query = queries.pop() if queries else Q()  # pop the first Q object from the list, or create an empty Q object if the list is empty
        for query in queries:
            combined_query |= query
        self.books_list = offered_books.filter(combined_query).order_by('-date')
        if not self.books_list:
            return offered_books
        return self.books_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['wished_books'] = self.wished_books
        if not self.books_list:
            context['nomatch'] = True
        context['filter_params'] = self.request.GET.get('filter')
        return context


class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['conditions'] = CONDITION
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = 'O'
        form.instance.active = True
        messages.success(self.request, "Offer Book successfully created")
        return super().form_valid(form)


class OfferEditView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/offer.html'
    form_class = BookForm

    def post(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            raise PermissionDenied()
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        book = get_object_or_404(self.model, pk=self.kwargs['pk'], status='O')
        return book

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['conditions'] = CONDITION
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)


class WishCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/wish.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = 'W'
        form.instance.active = True
        messages.success(self.request, "Wish Book successfully created")
        return super().form_valid(form)


class WishEditView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/wish.html'
    form_class = BookForm

    def post(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            raise PermissionDenied()
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        book = get_object_or_404(self.model, pk=self.kwargs['pk'], status='W')
        return book

    def form_valid(self, form):
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'

    # success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        raise Http404('GET method not allowed for this view.')

    def post(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            raise PermissionDenied()
        messages.success(request, f'{self.get_object().title} - {self.get_object().author} was deleted successfully')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER')
        if referer and 'offer' in referer:
            return reverse_lazy('offerlist')
        elif referer and 'wish' in referer:
            return reverse_lazy('wishlist')
        else:
            return reverse_lazy('home')


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.path.split('/')[-2] == 'wishlist':
            books = Book.objects.filter(owner=self.request.user, status='W').select_related('owner').order_by('-date')
            self.word = 'wish'
        elif self.request.path.split('/')[-2] == 'offerlist':
            books = Book.objects.filter(owner=self.request.user, status='O').select_related('owner').order_by('-date')
            self.word = 'offer'
        return books

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter_params'] = self.request.GET.get('filter')

        context['word'] = self.word
        return context

class AllBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'
    paginate_by = 5
    def get_queryset(self):
        books = Book.objects.all().select_related('owner')
        filter_params = self.request.GET.get('filter')  # region,education
        try:
            if filter_params == 'wish':
                books = books.filter(status='W')
            elif filter_params == 'offer':
                books = books.filter(status='O')
        except ValueError:
            pass
        return books
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter_params'] = self.request.GET.get('filter')
        context['word'] = 'all'

        return context
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
