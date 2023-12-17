import json
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import UserSerializer
from .serializers import ActivitySerializer, HospitalSerializer
from .models import Users, Hospital, Activity, Lookup
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import datetime
import jwt
from .getTokens import *
from .credentials import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# ------------------
from django.utils import timezone
from django.http import HttpResponse,QueryDict
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.http import QueryDict

# ------------------
class ActivityListView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get(self, request, *args, **kwargs):
        activities = self.get_queryset()
        serializer = self.serializer_class(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAccessView(generics.ListCreateAPIView):
    http_method_names = [
        "post",
        "get",
    ]
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if "sign-in" in request.path:
            return self.signin(request)
        elif "sign-up" in request.path:
            return self.signup(request)
        elif "sign-in-desktop" in request.path:
            return self.signin_desktop(request)
        # -------
        elif "activate" in request.path:
            return self.activate(request)
        # --------
        return Response({"message": "Invalid request."})

    def sigin_desktop(self,request):
        passwords_match = False
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
        except:
            body_data = request.body.decode('utf-8')
            query = QueryDict(body_data)
            email = query.get('email')
            password = query.get('password')
        all_objects = Users.objects.get(email=email)
        email_based_user = all_objects
        if email_based_user != None:
            passwords_match = check_password(password, email_based_user.password)
            if passwords_match == True:
                user = UserSerializer(all_objects)
                if user.data['is_authenticated_by_google'] == True:
                    lookup_value = Lookup.objects.get(id=user.data['user_type_id']).value
                    access_token, exp_time = getAccessToken(email=email)
                    refresh_token = getRefreshToken(email=email)
                    data = {
                        "access_token": access_token,
                        "exp_time": exp_time,
                        "refresh_token": refresh_token,
                        "user_type": lookup_value,
                        "profile_picture":user.data.profile_picture,
                        "username":user.data['user_name']
                    }
                    return Response(data , status=status.HTTP_200_OK)
                elif user.data['is_verified'] == True:
                    lookup_value = Lookup.objects.get(id=user.data['user_type']).value
                    access_token, exp_time = getAccessToken(email=email)
                    print(user.data)
                    refresh_token = getRefreshToken(email=email)
                    data = {
                        "access_token": access_token,
                        "exp_time": exp_time,
                        "refresh_token": refresh_token,
                        "user_type": lookup_value,
                        "profile_picture":user.data['profile_picture'],
                        "username":user.data['user_name']
                    }
                    return Response(data , status.HTTP_200_OK)
                
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    def signin(self, request):
        user_exists = False
        passwords_match = False
        
        if "user_name" in request.data:
            self.serializer_class.Meta.fields = ("user_name","email","password","is_authenticated_by_google")
        else:
            self.serializer_class.Meta.fields = ("email","password","is_authenticated_by_google")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            
            username = serializer.validated_data.get("user_name")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            IsAuthenticatedByGoogle = serializer.validated_data.get("is_authenticated_by_google")

            all_objects = Users.objects.filter(email=email)
            email_based_user = all_objects.first()
            if(email_based_user != None):
                passwords_match  = check_password(password , email_based_user.password)

            if IsAuthenticatedByGoogle == True:
                users = Users.objects.filter(
                    Q(user_name=username)
                    & Q(email=email)
                    & Q(is_authenticated_by_google=IsAuthenticatedByGoogle)
                    & Q(is_verified=True)
                )
                user_exists = Users.objects.filter(
                    Q(user_name=username)
                    & Q(email=email)
                    & Q(is_authenticated_by_google=IsAuthenticatedByGoogle)
                    & Q(is_verified=True)
                ).exists()

            elif((IsAuthenticatedByGoogle == False ) and (passwords_match == True) ):
                users = Users.objects.filter(
                    Q(email=email)
                    & Q(is_authenticated_by_google=IsAuthenticatedByGoogle)
                    & Q(is_verified=True)
                )
                user_exists = Users.objects.filter(
                    Q(email=email)
                    & Q(is_authenticated_by_google=IsAuthenticatedByGoogle)
                    & Q(is_verified=True)
                ).exists()
           
            if user_exists:
                user = users.first()
                lookup_value = Lookup.objects.get(id=user.user_type_id).value
                response = Response()
                access_token, exp_time = getAccessToken(serializer.data["email"])
                refresh_token = getRefreshToken(serializer.data["email"])
                self.serializer_class.Meta.fields = ("profile_picture","user_name","address" , "cnic", "contact","email" , 'date_of_birth',"first_name" , "last_name" ,'is_verified','is_authenticated_by_google','user_type','gender')
                email_based_user = UserSerializer(email_based_user)
                response.data = {
                    "access_token": access_token,
                    "exp_time": exp_time,
                    "refresh_token": refresh_token,
                    "user_type": lookup_value,
                    "username":email_based_user.data['user_name'],
                    "profile_picture":email_based_user.data['profile_picture']
                }
                response.status = status.HTTP_200_OK                
                return response

            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # -------------
    def activate(request , uidb64 , token ):

        email_delievering_time = float(token)
        expiration_time=604800

        current_time = timezone.now().timestamp()
        if( current_time - email_delievering_time > expiration_time ):
            message = "Email Verification Token Expired..."
            context = {'message': message}
            return render(request, 'temp.html',context)
        else:
            uid = urlsafe_base64_decode(uidb64).decode()
            print(uid)
            user = Users.objects.get(id=uid)
            print(user)

            try:
                user.is_verified = True
                user.save()  
                message = "User activated successfully..."
                context = {'message': message}
                return render(request, 'temp.html',context)
            except:
                message = "Failed to activate user..."
                context = {'message': message}
                return render(request, 'temp.html',context)
    # ----------

    def signup(self, request, userData=None):
        self.serializer_class.Meta.fields = "__all__"
        if userData == None:
            serializer = self.get_serializer(data=request.data)
        else:
            serializer = UserSerializer(data=userData)
        if serializer.is_valid():
            username = serializer.validated_data.get("user_name")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            isAuthenticatedByGoogle = serializer.validated_data.get(
                "is_authenticated_by_google"
            )

            username_exists = Users.objects.filter(Q(user_name=username)).exists()
            email_exists = Users.objects.filter(Q(email=email)).exists()
            if username_exists:
                return Response(
                    {"message": f"User with the username {username} already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif email_exists:
                return Response(
                    {"message": f"Email address is already taken."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            hashed_password = make_password(password)
            serializer.validated_data["password"] = hashed_password
            serializer.save()
            user = serializer.save()
            print(serializer)
            hospital = Hospital(name=username, owner=user)
            hospital.save()
            # # ------------------

            def activateEmail( request , user , toEmail):

                mail_subject = 'Activate your user acount'
                message = render_to_string('template_activate_account.html',{
                    'user':user.data['user_name'],
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.data['id'])),
                    # 'token':account_activation_token.make_token(user.data),
                    'token':timezone.now().timestamp(),
                    'protocol':'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message,to=[toEmail])
                email.content_subtype = "html"
                if(email.send()):
                    print("mail delivered")
                else:
                    print("mail not send")

            if isAuthenticatedByGoogle == False:
                activateEmail(request, serializer, email)
            # # ------------------
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
