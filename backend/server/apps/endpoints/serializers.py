# backend/server/apps/endpoints/serializers.py file
from rest_framework import serializers
from apps.endpoints.models import Endpoint
from apps.endpoints.models import SGAlgorithm
from apps.endpoints.models import SGAlgorithmStatus
from apps.endpoints.models import SGRequest

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields


class SGAlgorithmSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, mlalgorithm):
        return SGAlgorithmStatus.objects.filter(parent_sgalgorithm=sgalgorithm).latest('created_at').status

    class Meta:
        model = SGAlgorithm
        read_only_fields = ("id", "name", "description", "code",
                            "version", "owner", "created_at",
                            "parent_endpoint", "current_status")
        fields = read_only_fields

class SGAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SGAlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_by", "created_at",
                            "parent_sgalgorithm")

class SGRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SGRequest
        read_only_fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "created_at",
            "parent_sgalgorithm",
        )
        fields =  (
            "id",
            "input_data",
            "full_response",
            "response",
            "feedback",
            "created_at",
            "parent_sgalgorithm",
        )
