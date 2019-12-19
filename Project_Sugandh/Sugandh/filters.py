from .models import *
import django_filters

class customer_filter(django_filters.FilterSet):
    class Meta:
        model = customer_master
        fields = ['contact']

