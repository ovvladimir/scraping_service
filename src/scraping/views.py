from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, \
    DeleteView

from .forms import FindForm, VForm
from .models import Vacancy


def home_view(request):
    # qs = Vacancy.objects.all()
    # return render(request, 'scraping/home.html', {'object_list': qs})
    # print(request.GET)

    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})
