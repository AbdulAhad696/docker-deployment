from rest_framework.response import Response
from rest_framework import generics,status
from django.views.decorators.csrf import csrf_exempt
import jwt
from .credentials import *
from .getTokens import *
import jwt.exceptions as jwtex


class UpdateTokenView(generics.ListCreateAPIView):
    http_method_names = ['post']

    @csrf_exempt

    def post(self, request, *args, **kwargs):
        if 'updatetoken' in request.path:
            return self.updateToken(request)
        
    
    
    def updateToken(self,request):

        # refersh_token=request.COOKIES.get('refresh_token')
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header is not None :
            _, refersh_token = authorization_header.split(' ')
            try:
                
                email=decodeToken(refersh_token)
                print(email)
                new_access_token,exp_time=getAccessToken(email)
                new_refresh_token=getRefreshToken(email)

                response=Response()

                # response.set_cookie(key='refresh_token', value=new_refresh_token, httponly=True)
                response.data={
                    "access_token":new_access_token,
                    "exp_time":exp_time,
                    "refresh_token":new_refresh_token
                }
                response.status=status.HTTP_200_OK
                return response
            
            except jwtex.ExpiredSignatureError as error:
                return Response({'message':f'unauthorized user'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':f'unauthorized user'},status=status.HTTP_401_UNAUTHORIZED)
