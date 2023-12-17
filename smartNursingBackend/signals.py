from django.dispatch import Signal
from django.core.signals import got_request_exception
from django.dispatch import receiver

def my_exception_handler(sender, request, **kwargs):
    exception = kwargs['exception']
    # Your code here to handle the exception
    print(f"An exception occurred: {exception}")


update_signal = Signal()
