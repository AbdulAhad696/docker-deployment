from django.views.decorators.csrf import csrf_exempt



class CreateDb(generics.ListCreateAPIView):
    http_method_names = ['post']

    @csrf_exempt

    def post(self, request, *args, **kwargs):
        if 'createdb' in request.path:
            return self.createDb(request)
        
    
    
    def createDb(self,request):
        return 0

