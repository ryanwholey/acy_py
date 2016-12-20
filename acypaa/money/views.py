from django.shortcuts import render
from money.models import (
    Actual,
    Projected,
)
from money.serializers import (
    ActualSerializer,
    ProjectedSerializer,
)
from rest_framework import viewsets


class ActualViewSet(viewsets.ModelViewSet):
    queryset = Actual.objects.all().order_by('date')
    serializer_class = ActualSerializer


class ProjectedViewSet(viewsets.ModelViewSet):
    queryset = Projected.objects.all().order_by('date')
    serializer_class = ProjectedSerializer

