# file backend/server/apps/sg/registry.py
from apps.endpoints.models import Endpoint
from apps.endpoints.models import SGAlgorithm
from apps.endpoints.models import SGAlgorithmStatus

class SGRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                    algorithm_status, algorithm_version, owner,
                    algorithm_description, algorithm_code):
        # get endpoint
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        # get algorithm
        database_object, algorithm_created = SGAlgorithm.objects.get_or_create(
                name=algorithm_name,
                description=algorithm_description,
                code=algorithm_code,
                version=algorithm_version,
                owner=owner,
                parent_endpoint=endpoint)
        if algorithm_created:
            status = SGAlgorithmStatus(status = algorithm_status,
                                        created_by = owner,
                                        parent_sgalgorithm = database_object,
                                        active = True)
            status.save()

        # add to registry
        self.endpoints[database_object.id] = algorithm_object
