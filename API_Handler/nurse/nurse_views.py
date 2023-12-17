from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def testView(request):
    obj = {"message":"Nurse Test View"}
    return Response(obj)

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def emptyView(request):
    obj = {"message":"Empty View"}
    return Response(obj)