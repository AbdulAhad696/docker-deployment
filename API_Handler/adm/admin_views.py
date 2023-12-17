from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status, generics
from ..models import Patient,Users,Ward,Doctor,Nurse
from ..serializers import PatientSerializer, DoctorSerializer, NurseSerializer,WardSerializer
from utils import common_utils
from ..user_access import UserAccessView
from django.db.models import Q
from django.db import transaction
from django.db import connection
from ..getTokens import *

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def testView(request):
    obj = {"message":"Admin Test View"}
    return Response(obj)

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    def get(self, request, *args, **kwargs):
        # allow only limited knowledge about the patient to the admin
        print(request.query_params)
        if 'wardName' in request.query_params:
            obj = {"message":"Admin GET WARD View"}
            # wards = Ward.objects.filter(Q(Name=request.query_params['wardName'])).exists()
            patients_with_wards = Patient.objects.select_related('Ward').all()
            serializer = self.serializer_class(patients_with_wards, many=True)
        else:
            obj = {"message":"Admin GET ALL View"}
        return Response(serializer.data)

    def post(self, request):
        try:
            if "contact" not in request.data or "email" not in request.data:
                return Response({"message":"Missing contact information"}, status=status.HTTP_400_BAD_REQUEST)
            if 'Gender' not in request.data:
                return Response({"message":"Missing Gender"}, status=status.HTTP_400_BAD_REQUEST)
            if 'Fname' not in request.data or 'Lname' not in request.data:
                return Response({"message":"Missing Name of Patient"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                username = common_utils.generate_username(request.data['Fname'], request.data['Lname'])
                password = common_utils.generate_random_password()
                userData = {
                    "username":username,
                    "password":password,
                    "email":request.data['email'],
                    "contact":request.data['contact'],
                    "Fname":request.data['Fname'],
                    "Lname":request.data['Lname'],
                    "usertype":2,
                    "Gender":request.data['Gender']
                }
                with transaction.atomic():
                    response = UserAccessView.signup(self,request,userData=userData)

                    if "message" not in response.data:
                        # serializer.validated_data['UserId'] = response.data['id']

                        # Get the Users instance
                        user_instance = Users.objects.get(id=response.data['id'])

                        # Assign the Users instance to UserId field in the Patient model
                        serializer.validated_data['UserId'] = user_instance
                        
                        serializer.save()
                        return Response({"message": "Patient Profile Created"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message": "Failed to create Patient Profile. "+response.data['message']}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PatientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        patient_id = request.query_params.get('patientId')

        if patient_id is None:
            return Response({"message": "Missing Patient ID query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                patient_instance = self.get_queryset().filter(Q(id=patient_id)).first() 

                if patient_instance is not None: 
                    user = patient_instance.UserId_id
                    print(user)
                    patient_instance.delete()  
                    
                    try:
                        user_instance = Users.objects.get(pk=user)
                        user_instance.delete()  
                    except Users.DoesNotExist:
                        # user might have been deleted through cascade
                        pass  

                    return Response({"message": f"Patient and associated user deleted"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"message": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({"message": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        
class AdminDashboard(generics.ListCreateAPIView):
    patient_serializer = PatientSerializer
    doctor_serializer = DoctorSerializer
    nurse_serializer =  NurseSerializer
    ward_serializer = WardSerializer

    def post(self,request):
        
        try:
            token = request.headers.get('Authorization')
            _, access_token = token.split(' ')
            try:
                email = decodeToken(access_token)
                try:
                    with transaction.atomic():
                        with connection.cursor() as cursor:
                            # use the email to get the owner id of hospital
                            cursor.execute('SELECT id FROM public."API_Handler_hospital" WHERE owner_id = (SELECT id FROM public."API_Handler_users" WHERE email = %s);',[email])
                            hospital = cursor.fetchone()[0]
                            # use the hospital id to get the ward id from HospitalWard
                            cursor.execute('SELECT id FROM public."API_Handler_ward" WHERE hospital_id = %s;',[hospital])
                            ward_ids = cursor.fetchall()
                            # print("Ward IDs: ",ward_ids)
                            # use the ward ids to count the patient ids from patient
                            cursor.execute('SELECT COUNT(*) FROM public."API_Handler_patient" WHERE ward_id IN %s;',[tuple(ward_ids)])
                            patient_count = cursor.fetchall()
                            # print("Patient Count: ",patient_count)
                            # use the ward ids to get the doctor ids from doctorward
                            cursor.execute('SELECT doctor_id FROM public."API_Handler_doctorward" WHERE ward_id IN %s;',[tuple(ward_ids)])
                            doctor_list = cursor.fetchall()
                            doctor_count = len(doctor_list)
                            # print("Doctor Count: ",doctor_count)
                            # print("Doctor List: ",doctor_list)
                            # use the ward ids to count the nurse ids from nurse
                            cursor.execute('SELECT COUNT(nurse_id) FROM public."API_Handler_nurseward" WHERE ward_id IN %s;',[tuple(ward_ids)])
                            nurse_count = cursor.fetchone()[0]
                            # print("Nurse Count: ",nurse_count)
                            # use the ward ids to get the ward names from ward
                            cursor.execute('SELECT * FROM public."API_Handler_ward" WHERE id IN %s;',[tuple(ward_ids)])
                            ward_data = cursor.fetchall()
                            ward_count = len(ward_data)
                            # print("Ward Count: ",ward_count)
                            # print("Ward Data: ",ward_data)
                            # use the doctor_list to Group and count the domains
                            cursor.execute('SELECT domain_count, value as domain_name FROM (SELECT domain_id, COUNT(domain_id) AS domain_count FROM public."API_Handler_doctor" WHERE id IN %s GROUP BY domain_id) as tab1 JOIN public."API_Handler_lookup" lookup on lookup.id = tab1.domain_id;',[tuple(doctor_list)])
                            domain_data = cursor.fetchall()
                            # print("Domain Data: ",domain_data)
                            # Extract the number of admitted patients
                            cursor.execute('SELECT COUNT(*) FROM public."API_Handler_patient" WHERE discharge_date IS NULL AND ward_id IN %s;',[tuple(ward_ids)])
                            admitted_patients = cursor.fetchone()[0]
                            # print("Admitted Patients: ",admitted_patients)
                            # Extract the number of discharged patients
                            cursor.execute('SELECT COUNT(*) FROM public."API_Handler_patient" WHERE discharge_date IS NOT NULL AND ward_id IN %s;',[tuple(ward_ids)])
                            discharged_patients = cursor.fetchone()[0]
                            # print("Discharged Patients: ",discharged_patients)
                            # Extract the ratio of patients in this hospital who are new and old and total patients that are admitted
                            cursor.execute(
                                '''
                                SELECT COUNT(new_patients.user_id) AS new_patient_count, COUNT(old_patients.user_id) as old_patient_count, COUNT (all_patients.user_id) as total_patients
                                FROM (
                                    SELECT DISTINCT user_id FROM public."API_Handler_patient" WHERE ward_id IN %s
                                ) as all_patients
                                LEFT JOIN(
                                    SELECT user_id FROM public."API_Handler_patient" WHERE ward_id in %s GROUP BY user_id HAVING COUNT(user_id)=1
                                ) as new_patients ON all_patients.user_id = new_patients.user_id
                                LEFT JOIN (
                                    SELECT user_id FROM public."API_Handler_patient" WHERE ward_id in %s GROUP BY user_id HAVING COUNT(user_id)>1
                                ) as old_patients on all_patients.user_id = old_patients.user_id
                                ''',[tuple(ward_ids)]*3
                            )
                            new_old_total_ratio = cursor.fetchall()
                            # print("New Old Total Ratio: ",new_old_total_ratio)
                            return Response({"message": "Request Received",
                            "Response":{"CardData":[{
                                                    "CardTitle":"Patients",
                                                    "Count":patient_count,
                                                    "Icon":"Patient"
                                                },{
                                                    "CardTitle":"Doctors",
                                                    "Count":doctor_count,
                                                    "Icon":"Doctor"
                                                },{
                                                    "CardTitle":"Nurses",
                                                    "Count":nurse_count,
                                                    "Icon":"Nurse"
                                                },{
                                                    "CardTitle":"Wards",
                                                    "Count":ward_count,
                                                    "Icon":"Ward"
                                                },{
                                                    "CardTitle":"Admitted",
                                                    "Count":admitted_patients,
                                                    "Icon":"Admit"
                                                },{
                                                    "CardTitle":"Discharged",
                                                    "Count":discharged_patients,
                                                    "Icon":"Left"
                                                },
                                                ], 
                                        "WardData":ward_data,
                                        "DomainData":domain_data,
                                        "PatientRatios":new_old_total_ratio
                                        }}, status=status.HTTP_200_OK)
                except Exception as e:
                    print("Error in retrieving dashboard data",e)
                    return Response({"message":"Failed to retrieve data. Internal Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            except Exception as e:
                print("Failed to decode access token. Error: ", e)
                return Response({"message":"Error in decoding the access token"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("Error splitting the auth token",e)
            return Response({"message":"Error splitting the auth token"},status=status.HTTP_401_UNAUTHORIZED)
            