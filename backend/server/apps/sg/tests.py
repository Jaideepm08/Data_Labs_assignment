import inspect
from apps.sg.registry import SGRegistry
from django.test import TestCase

from apps.sg.sun_glare_algo.sun_glare import SunGlareAlgorithm

class SGTests(TestCase):
    def test_sg_algorithm(self):
        self.input_data = {
            "lat": 89788,
            "lon": -987887,
            "epoch": 34146,
            "orientation": 6786969,
        }
        my_alg = SunGlareAlgorithm()
        response = my_alg.predict(self.input_data)
        self.assertEqual('ok', response['status'])
        #self.assertTrue('label' in response)
        #self.assertEqual('<=50K', response['label'])

    def test_registry(self):
        registry = SGRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "sun_glare_algo"
        algorithm_object = SunGlareAlgorithm()
        algorithm_name = "sun glare"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Jai"
        algorithm_description = "Sun glare detection for cars"
        algorithm_code = inspect.getsource(SunGlareAlgorithm)
        # add to registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                    algorithm_status, algorithm_version, algorithm_owner,
                    algorithm_description, algorithm_code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)
