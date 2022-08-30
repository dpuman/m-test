import django_filters
from .models import Product
from django import forms


class ProductFilter(django_filters.FilterSet):

    fromPrice = django_filters.NumberFilter(
        field_name='productvariantprice__price', lookup_expr='gte', widget=forms.NumberInput(attrs={'class': 'newClass form-control', 'placeholder': 'From'}))
    toPrice = django_filters.NumberFilter(
        field_name='productvariantprice__price', lookup_expr='lt', widget=forms.NumberInput(attrs={'class': 'newClass form-control', 'placeholder': 'To'}))

    date = django_filters.DateFilter(
        field_name='created_at', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    title = django_filters.CharFilter(
        'title', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'newClass form-control', 'placeholder': 'Product title'}))

    class Meta:
        model = Product
        fields = ['title']
