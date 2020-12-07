from django.shortcuts import render

# Create your views here.
# backend/server/apps/endpoints/views.py file
from rest_framework import viewsets
from rest_framework import mixins

from apps.endpoints.models import Endpoint
from apps.endpoints.serializers import EndpointSerializer

from apps.endpoints.models import SGAlgorithm
from apps.endpoints.serializers import SGAlgorithmSerializer

from apps.endpoints.models import SGAlgorithmStatus
from apps.endpoints.serializers import SGAlgorithmStatusSerializer

from apps.endpoints.models import SGRequest
from apps.endpoints.serializers import SGRequestSerializer

class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class SGAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SGAlgorithmSerializer
    queryset = SGAlgorithm.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = SGAlgorithmStatus.objects.filter(parent_sgalgorithm = instance.parent_sgalgorithm,
                                                        created_at__lt=instance.created_at,
                                                        active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    SGAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

class SGAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin):
    serializer_class = SGAlgorithmStatusSerializer
    queryset = SGAlgorithmStatus.objects.all()
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)



        except Exception as e:
            raise APIException(str(e))

class SGRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin):
    serializer_class = SGRequestSerializer
    queryset = SGRequest.objects.all()
