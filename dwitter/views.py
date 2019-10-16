from django.contrib.auth.models import User
from django_filters import FilterSet, NumberFilter, CharFilter
from django.shortcuts import render
from django.utils import timezone
from dwitter.models import Comment, Dweet
from dwitter.permissions import IsAuthorOrReadOnly

def about(request):
    return render(request, 'about.html', {'show_submit_box': True})