from ..models import Doctor, Users, Lookup, Hospital,DoctorWard , Ward
from ..serializers import DoctorSerializer, LookupSerializer, UserSerializer , DoctorWardSerializer,WardSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics,status
import google.generativeai as palm
from API_Handler import credentials as cr
from ..getTokens import *
from ..views import *
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.contrib.auth.hashers import make_password
from datetime import datetime

class QueryBard(generics.CreateAPIView):
    palm.configure(api_key=cr.bard_api)
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    def post(self, request, *args, **kwargs):
        print("Querying bard")
        token = request.headers.get('Authorization')
        if token is not None :
            _, access_token = token.split(' ')
            try:
                email = decodeToken(access_token)
                numRecords = request.data['records']
                patientData = request.data['patientData']
                  # indent for pretty printing
                for tup in patientData:
                    
                    parsed_timestamp = datetime.datetime.strptime(tup['time'], '%Y-%m-%dT%H:%M:%SZ')

                    # Format the parsed timestamp in a human-readable format
                    tup['time'] = parsed_timestamp.strftime('%Y-%m-%d %I:%M:%S %p')
                # Print or use the formatted JSON string
                formatted_json = json.dumps(patientData, indent=2)
                # Call Bard
                query = request.data['query']
                completeQuery =  query + formatted_json
                
                
                completion = palm.generate_text(
                    model=self.model,
                    prompt=completeQuery,
                    temperature=0.05,
                    # The maximum length of the response
                    max_output_tokens=250,
                )
                # print("Completions:",completion.result)
                print(completeQuery)
                print(completion.result)
                if completion.result is None:
                    randomness=0.1
                    newTemp=0.05
                    while completion.result is not None or newTemp<0.5:
                        newTemp +=randomness
                        print("processing")
                        completion = palm.generate_text(
                            model=self.model,
                            prompt=completeQuery,
                            temperature=newTemp,
                            # The maximum length of the response
                            max_output_tokens=250,
                        )
                    if completion.result is None:
                        completion.result = "Unable to answer your query at the moment. Please Try again later"
                    print("Completions:",completion.result)
                return JsonResponse({"response":completion.result})
            except Exception as e:
                print("Exception:",e)
                return JsonResponse({"response":str(e)})
        print("Failed to decode")    
        return JsonResponse({"response":"An Error Occured","status":status.HTTP_400_BAD_REQUEST})
        
    
    

import json
import random
from ..getTokens import *

@api_view(['POST'])
def delete_doctor(request):
    if request.method == "POST":
        doctors_id_array = request.body
        string_representation = doctors_id_array.decode('utf-8')
        # Remove square brackets and split the string into a list of strings
        numeric_strings = string_representation[1:-1].split(',')

        # Convert each string to an integer
        doctors_id_array = [int(num_str) for num_str in numeric_strings]
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        # authorization_header = None
        if authorization_header is not None:
            _, refersh_token = authorization_header.split(" ")
            admin_email = decodeToken(refersh_token)
            try:
                for doctor_id in doctors_id_array:
                    deleted_count , _ = Doctor.objects.filter(id = doctor_id).delete()
                return JsonResponse({"message": f"{deleted_count} doctors deleted successfully"})
            except Exception as e:
            # Handle exceptions, such as invalid IDs or database errors
                return JsonResponse({"error": f"Error: {str(e)}"})    
        else:
            return JsonResponse({"message": "unauthorized_user"})


@api_view(["POST"])
def get_hospital_doctors(request):
    if request.method == "POST":
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        # authorization_header = None
        if authorization_header is not None:
            _, refersh_token = authorization_header.split(" ")
            admin_email = decodeToken(refersh_token)
            adminId = Users.objects.get(email=admin_email)
            hospitalId = Hospital.objects.get(
                    owner=adminId
                )
            wards = Ward.objects.filter(hospital=hospitalId)
            doctors = DoctorWard.objects.filter(ward__in = wards)
            # doctors = Doctor.objects.filter(hospital=hospitalId)
            ## Get all the doctors from DB
            ## Convert the python object into a JSON object using a serializer
            serializer = DoctorWardSerializer(doctors , many=True)
            ## If we have doctors in the DB, then return it
            # print(serializer.data)
            data = serializer.data
            if (len(data)) > 0:
                return JsonResponse({"doctors": data})
            ## Else return that we couldn't find any of the doctors
            return JsonResponse({"doctors": "Not Found"}) # 204 No Content
        else:
            return JsonResponse({"message": "unauthorized_user"})

@api_view(["POST"])
def get_domains_wards(request):
    if request.method == "POST":
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        # authorization_header = None
        if authorization_header is not None:
            _, refersh_token = authorization_header.split(" ")
            domains = Lookup.objects.filter(type = "doctor_domain")
            admin_email = decodeToken(refersh_token)
            adminId = Users.objects.get(email=admin_email)
            hospitalId = Hospital.objects.get(owner=adminId)    
            wards = Ward.objects.filter(hospital = hospitalId)
            serializeDomains = LookupSerializer(domains , many= True)
            serializeWards = WardSerializer(wards,many=True)
            data = {"domains":serializeDomains.data,"wards":serializeWards.data}
            return JsonResponse(data)
            ## Else return that we couldn't find any of the doctors
        else:
            return JsonResponse({"message": "unauthorized_user"})

@api_view(["POST"])
def get_doctors_domains(request):
    if request.method == "POST":
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        # authorization_header = None
        if authorization_header is not None:
            _, refersh_token = authorization_header.split(" ")
            # admin_email = decodeToken(refersh_token)
            domains = Lookup.objects.filter(type = "doctor_domain")
            ## Get all the doctors from DB
            ## Convert the python object into a JSON object using a serializer
            serializer = LookupSerializer(domains, many=True)
            ## If we have doctors in the DB, then return it
            print(serializer.data)
            if (len(serializer.data)) > 0:
                return JsonResponse({"domains": serializer.data})
            ## Else return that we couldn't find any of the doctors
            return JsonResponse({"domains": "Not Found"}) # 204 No Content
        else:
            return JsonResponse({"message": "unauthorized_user"})

@api_view(["POST"])
def get_hospital_ward(request):
    if request.method == "POST":
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        # authorization_header = None
        if authorization_header is not None:
            _, refersh_token = authorization_header.split(" ")
            admin_email = decodeToken(refersh_token)
            adminId = Users.objects.get(email=admin_email)
            hospitalId = Hospital.objects.get(owner=adminId)    
            wards = Ward.objects.filter(hospital = hospitalId)
            serializer = WardSerializer(wards, many=True)
            ## If we have doctors in the DB, then return it
            print(serializer.data)
            if (len(serializer.data)) > 0:
                return JsonResponse({"wards": serializer.data})
            ## Else return that we couldn't find any of the doctors
            return JsonResponse({"wards": "Not Found"}) # 204 No Content
        else:
            return JsonResponse({"message": "unauthorized_user"})

@api_view(["POST"])
def get_doctor_by_id(request):
    if request.method == "POST":
        data = json.loads(request.body)
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        # authorization_header = None
        if authorization_header is not None:
            _, refersh_token = authorization_header.split(" ")
            doctors = Doctor.objects.filter(id=data.get('id')).first()
            ## Get all the doctors from DB
            ## Convert the python object into a JSON object using a serializer
            doctorWards = DoctorWard.objects.filter(doctor = doctors)
            doctorWardsSerializer = DoctorWardSerializer(doctorWards,many=True)
            serializer = DoctorSerializer(doctors)
            ## If we have doctors in the DB, then return it
            print(serializer.data)
            if (len(serializer.data)) > 0:
                tempSerializer = serializer.data
                tempSerializer["wards"] = doctorWardsSerializer.data
                return JsonResponse({"doctors": tempSerializer})
            ## Else return that we couldn't find any of the doctors
            return JsonResponse({"doctors": "Not Found"}) # 204 No Content
        else:
            return JsonResponse({"message": "unauthorized_user"})
@api_view(['PUT'])
def update_doctor(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        gender = data.get("gender")
        domain = data.get("domain")
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            return Response({"message": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            gender_lookup = Lookup.objects.get(value = gender)
        except Lookup.DoesNotExist:
            return Response({"message": "Gender Not Found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            domain_lookup = Lookup.objects.get(value = domain)
        except Lookup.DoesNotExist:
            return Response({"message": "Domain Not Found"}, status=status.HTTP_404_NOT_FOUND)
        if request.method == "PUT": 
            data = json.loads(request.body)
            authorization_header = request.META.get("HTTP_AUTHORIZATION")
            # authorization_header = None
            if authorization_header is not None:
                _, refersh_token = authorization_header.split(" ")
                admin_email = decodeToken(refersh_token)
                # Assuming data is sent in the same format as the add_doctor API
                date_of_birth = data.get("date_of_birth")
                contact = data.get("contact")
                first_name, last_name = data.get("first_name"), data.get("last_name")
                wards = data.get('wards')
                address = data.get("address") or ""
                domain = data.get("domain") or ""
                cnic = data.get("cnic") or ""
                # password = "123"  # You might want to handle this differently

                # Update User model
                user = doctor.user
                # user.email = email
                user.date_of_birth = date_of_birth
                user.contact = contact
                user.first_name = first_name
                user.gender = gender_lookup
                user.last_name = last_name
                user.address = address
                user.cnic = cnic
                user.save()

                # Update Doctor model
                doctor.domain = domain_lookup
                doctor.save()

                # Update associated wards
                doctorWard = DoctorWard.objects.filter(doctor=doctor).delete()
                
                adminId = Users.objects.get(email=admin_email)
                hospitalId = Hospital.objects.get(
                        owner=adminId
                    )
                for ward in wards:
                    ward_obj = Ward.objects.get(name=ward, hospital=hospitalId)
                    doctorWard = DoctorWard(doctor=doctor, ward=ward_obj)
                    doctorWard.save()

                # updated_doctor = Doctor.objects.get(pk=pk)
                serializer = DoctorSerializer(doctor)
                return Response({"doctor": serializer.data})
            else:
                return JsonResponse({"message": "unauthorized_user"})
    except:
        return JsonResponse({"message": "Internal Server Error"})
@api_view(["POST"])
def add_doctor(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Send Password to the doctor on the email
        # that he has been registered on
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        if authorization_header is not None:
            try:
                _, refersh_token = authorization_header.split(" ")
                admin_email = decodeToken(refersh_token)
                # print(admin_email)
                # admin_email = "sh@gmail.com"
                password = "123"
                email = data.get("email")
                userType = "doctor"
                date_of_birth = data.get("date_of_birth")
                contact = data.get("contact")
                first_name, last_name = data.get("first_name"), data.get("last_name")
                wards = data.get('wards')
                genderType = data.get("gender")
                address = data.get("address") or ""
                domain = data.get("domain") or ""
                cnic = data.get("cnic") or ""
                username = first_name + "_" + last_name + str(random.randint(1, 100))

                doctor_exist = Users.objects.filter(email=email).exists()
                if doctor_exist:
                    return JsonResponse({"message": "Email already exist"})
                # Generating UNique Random User Names
                while Users.objects.filter(user_name=username).exists():
                    username = first_name + "_" + last_name + str(random.randint(1, 100))
                # Finding the values for gender and usertype in Lookup
                userType_from_lookup = Lookup.objects.get(value=str(userType).lower())
                domain_from_lookup = Lookup.objects.get(value=str(domain))
                userGender_from_lookup = Lookup.objects.get(
                    value=str(genderType).lower()
                )
                hashed_password = make_password(password)
                # Creating an instance of User
                user = Users(
                    user_name=username,
                    cnic=cnic,
                    email=email,
                    password=hashed_password,
                    user_type=userType_from_lookup,
                    contact=contact,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    gender=userGender_from_lookup,
                    is_authenticated_by_google=False,
                    date_of_birth=date_of_birth
                )
                user.save()
                adminId = Users.objects.get(email=admin_email)
                hospital = Hospital.objects.get(
                    owner=adminId
                )
                doctor = Doctor(user=user, domain=domain_from_lookup)
                doctor.save()

                for ward in wards:
                    ward_obj = Ward.objects.get(name=ward , hospital=hospital)
                    doctorWard = DoctorWard(doctor = doctor,ward = ward_obj) 
                    doctorWard.save()
                # Assuming there's a direct link between Hospital and User
                # Creating an instance of Doctor

                doctor = DoctorSerializer(doctor)
                

                return JsonResponse({"doctor": doctor.data})
            except Exception as e:
                return JsonResponse({"message": "Internal Server Error"})
        else:
            return JsonResponse({"message": "unauthorized_user"}) 
