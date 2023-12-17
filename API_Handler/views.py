from django.shortcuts import render
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import influxdb_client
from django.http import HttpResponse
import datetime
import logging
from smartNursingBackend.settings import logger
newLogFileNamesArray = []
from influxdb_client import InfluxDBClient, Point
from .getTokens import *
import urllib.parse
from logging.handlers import TimedRotatingFileHandler
# import status codes from django rest framework
from rest_framework import status

logname = "logs/logsContainer.log"
handler = TimedRotatingFileHandler(logname, when="midnight", backupCount=30)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)


# ---------Credentials of influxdb-------------
databucket = "Object Detection"
bucket = "Object Detection"
org = "1936be69c64da4d7"
token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

measurement = "User"
client = InfluxDBClient(url=url, token=token, org=org)

    
def index(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    now = datetime.datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

def count_influx(request):
    logger.warning('Count sent  '+str(datetime.datetime.now())+' hours!')
    query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> count()'
    result = client.query_api().query(query)
    try:
        response = result[0].records[0].values['_value']
    except Exception as e:
        response = 0
        print(e)
    return HttpResponse(response)


def fetch_from_influx(request):
    logger.warning('Accessing objects '+str(datetime.datetime.now())+' hours!')
    try:
        query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")|> sort(columns: ["_time"], desc: true)|>limit(n: 100)'
        result = client.query_api().query(query)
        json_result = []
        for table in result:
            for record in table.records:
                # Get timestamp from FluxRecord object
                record_time = record.get_time().strftime('%Y-%m-%dT%H:%M:%SZ')
                record_values = record.values
                # Add time field to record_values dictionary
                record_values['time'] = record_time
                json_result.append(record_values)
        return JsonResponse(json_result,safe=False)
    except Exception as e:
        
        print("Exception: ",e)
        logger.warning("Error in fetching data from influx" + str(datetime.datetime.now())+' hours!')
        return JsonResponse({'message':"Error Sending Response"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def fetchUserSpecificData(request, *args, **kwargs):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    # authorization_header = "bearer key"
    if authorization_header is not None :
        _, access_token = authorization_header.split(' ')
        logger.warning('Accessing objects with User Id'+str(datetime.datetime.now())+' hours!')
        try:
            email = str(decodeToken(access_token))
            query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "activityDetection")|> filter(fn: (r) => r.HospitalID == "{email}") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")|> sort(columns: ["_time"], desc: true)|>limit(n: 100)'
            result = client.query_api().query(query)

            json_result2 = []
            for table in result:
                for record in table.records:
                    # Get timestamp from FluxRecord object
                    record_time = record.get_time().strftime('%Y-%m-%dT%H:%M:%SZ')
                    record_values = record.values
                    # Add time field to record_values dictionary
                    record_values['time'] = record_time
                    json_result2.append(record_values)
            output = json_result2
            return JsonResponse(output,safe=False)
        except Exception as e:
            logger.warning("Error in fetching data from influx" + str(datetime.datetime.now())+' hours!')
            return JsonResponse({'message':"Error Fetching Data. Internal Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse({'message':"Auth token failed"},status=404)

def fetch_images_ids(request):
    query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "ImagesOnDrive")|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")|> sort(columns: ["_time"], desc: true)|>limit(n: 10)'
    result = client.query_api().query(query)
    json_result=[]
    imageIdArray=[]
    for table in result:
        for record in table.records:
            # Get timestamp from FluxRecord object
            record_time = record.get_time().strftime('%Y-%m-%dT%H:%M:%SZ')
            record_values = record.values
            # Add time field to record_values dictionary
            record_values['time'] = record_time
            json_result.append(record_values)

    return JsonResponse(json_result,safe=False)