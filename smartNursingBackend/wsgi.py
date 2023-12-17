"""
WSGI config for vercel_app project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import os
import atexit
from smartNursingBackend.pusher_client import initPusher,killPusher
from smartNursingBackend.mqtt_receive import HiveMqtt
from django.core.wsgi import get_wsgi_application
from smartNursingBackend.my_logger import myThread1

def cleanup_function():
    # mqinstance = HiveMqtt()
    # mqinstance.killClient()
    killPusher()
    print("Application terminated. Performing cleanup.")


atexit.register(cleanup_function)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartNursingBackend.settings')

app = get_wsgi_application()
initPusher()
# mqinstance = HiveMqtt()
# Start the thread
myThread1.start()
