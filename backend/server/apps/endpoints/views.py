import json
from numpy.random import rand
from rest_framework import views, status
from rest_framework.response import Response
from apps.sg.registry import SGRegistry
from server.wsgi import registry

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


class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")
        #SGAlgorithm.objects.filter(id=2).delete()

        algs = SGAlgorithm.objects.filter(parent_endpoint__name = endpoint_name, status__status = algorithm_status, status__active=True)

        if algorithm_version is not None:
            algs = algs.filter(version = algorithm_version)

        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "SG algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(algs)
        print("len is",len(algs))
        if len(algs) != 1 and algorithm_status != "ab_testing":
           return Response(
               {"status": "Error", "message": "SG algorithm selection is ambiguous. Please specify algorithm version."},
               status=status.HTTP_400_BAD_REQUEST,
           )
        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if rand() < 0.5 else 1

        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.predict(request.data)


        label = prediction["label"] if "label" in prediction else "error"
        sg_request = SGRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_sgalgorithm=algs[alg_index],
        )
        sg_request.save()

        prediction["request_id"] = sg_request.id

        return Response(prediction)
