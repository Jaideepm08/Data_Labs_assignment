"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = get_wsgi_application()
# SG registry
import inspect
from apps.sg.registry import SGRegistry
from apps.sg.sun_glare_algo.sun_glare import SunGlareAlgorithm

try:
    registry = SGRegistry() # create ML registry
    input_data ={"lat":987}
    # Sun glare algorithm
    sg = SunGlareAlgorithm(input_data)
    # add to SG registry
    registry.add_algorithm(endpoint_name="sun_glare_algo",
                            algorithm_object=sg,
                            algorithm_name="sun glare",
                            algorithm_status="production",
                            algorithm_version="0.0.1",
                            owner="Jai",
                            algorithm_description="Sun Glare Algorithm",
                            algorithm_code=inspect.getsource(SunGlareAlgorithm))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
