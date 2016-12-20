from django.conf.urls import (
    url,
    include,
)
from rest_framework import routers
from .views import (
    ActualViewSet,
    ProjectedViewSet,
)

router = routers.DefaultRouter()
router.register(r'actual', ActualViewSet)
router.register(r'projected', ProjectedViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^transactions/projected/$', ProjectedViewSet),
]