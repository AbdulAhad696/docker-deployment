from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from ..serializers import PatientSerializer
from ..models import Patient
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from smartNursingBackend.settings import logger


from rest_framework.response import Response
from rest_framework import generics, status
from django.views.decorators.csrf import csrf_exempt
import jwt
from ..credentials import *
from ..getTokens import *
from jwt.exceptions import ExpiredSignatureError


class PatientAccessView(generics.ListCreateAPIView):
    http_method_names = [
        "post",
    ]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if "patient-register" in request.path:
            return self.addingPatientsData(request)
        return Response({"message": "Invalid request."})

    def addingPatientsData(self, request):
        # authorization_header = request.META.get("HTTP_AUTHORIZATION")
        # if authorization_header is not None:
        #     _, refersh_token = authorization_header.split(" ")
        #     try:
        #         email = decodeToken(refersh_token)
        #     except:
        #         pass
        # logger.warning("${email} has registered patient")

        # self.serializer_class.Meta.fields = "__all__"
        # if patientData == None:
        #     serializer = self.get_serializer(data=request.data)
        # else:
        #     serializer = PatientSerializer(data=patientData)

        # if serializer.is_valid():
        #     id = serializer.validated_data.get("id")
        #     age = serializer.validated_data.get("age")
        #     blood_group = serializer.validated_data.get("blood_group")
        #     height = serializer.validated_data.get("height")
        #     weight = serializer.validated_data.get("weight")
        #     # BMI = str(int(weight)/(int(height) * int(height)))
        #     bmi = serializer.validated_data.get("bmi")

        #     systolic_bp = serializer.validated_data.get("systolic_bp")
        #     diastolic_bp = serializer.validated_data.get("diastolic_bp")
        #     heart_beat = serializer.validated_data.get("heart_beat")
        #     temperature = serializer.validated_data.get("temperature")
        #     o2_level = serializer.validated_data.get("o2_level")
        #     ward = serializer.validated_data.get("ward")
        #     nursing_diagnosis = serializer.validated_data.get("NursingDiagnosis")
        #     medical_diagnosis = serializer.validated_data.get("MedicalDiagnosis")
        #     cnic = serializer.validated_data.get("cnic")
        #     hospitalization = serializer.validated_data.get("hospitalization")
        #     major_illness = serializer.validated_data.get("major_illness")
        #     surgeries = serializer.validated_data.get("Surgeries")
        #     pain_location = serializer.validated_data.get("pain_location")
        #     pain_severity = serializer.validated_data.get("pain_severity")
        #     current_medication = serializer.validated_data.get("current_medication")
        #     past_medication = serializer.validated_data.get("past_medication")
        #     supplements = serializer.validated_data.get("supplements")
        #     medical_allergy = serializer.validated_data.get("medical_allergy")

        #     serializer.save()
        try:
            patient=Patient.objects.get(id=request.data["id"])
            if(patient):
                patient.blood_group=request.data["blood_group"]
                patient.height=request.data["height"]
                patient.weight=request.data["weight"]
                patient.bmi=request.data["bmi"]
                patient.systolic_bp=request.data["systolic_bp"]
                patient.diastolic_bp=request.data["diastolic_bp"]
                patient.heart_beat=request.data["heart_beat"]
                patient.temperature=request.data["temperature"]
                patient.o2_level=request.data["o2_level"]
                patient.hospitalization=request.data["hospitalization"]
                patient.major_illness=request.data["major_illness"]
                patient.surgeries=request.data["surgeries"]
                patient.pain_location=request.data["pain_location"]
                patient.pain_severity=request.data["pain_severity"]
                patient.current_medication=request.data["current_medication"]
                patient.past_medication=request.data["past_medication"]
                patient.supplements=request.data["supplements"]
                patient.medical_allergy=request.data["medical_allergy"]
                patient.save()
                return Response("Success", status=status.HTTP_201_CREATED)

            else:
                return Response("Error", status=status.HTTP_400_BAD_REQUEST)


            # return Response(serializer.data, status=status.HTTP_201_CREATED)


        except:
            # print(serializer.errors)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)

