# backend/server/apps/endpoints/urls.py file
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.endpoints.views import EndpointViewSet
from apps.endpoints.views import SGAlgorithmViewSet
from apps.endpoints.views import SGAlgorithmStatusViewSet
from apps.endpoints.views import SGRequestViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"sgalgorithms", SGAlgorithmViewSet, basename="sgalgorithms")
router.register(r"sgalgorithmstatuses", SGAlgorithmStatusViewSet, basename="sgalgorithmstatuses")
router.register(r"sgrequests", SGRequestViewSet, basename="sgrequests")

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
]
