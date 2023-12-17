
from django.views.decorators.csrf import csrf_exempt
from smartNursingBackend.settings import logger
import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json

# ---------Credentials of influxdb-------------
databucket = "Object Detection"
org = "1936be69c64da4d7"
token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
measurement = "User"
client = InfluxDBClient(url=url, token=token, org=org)



def getSpecificUser(request, *args, **kwargs):
    logger.warning('Attempt to sign in user  '+str(datetime.datetime.now())+' hours!')
    try:
        # --------using glpbal variables--------
        global bucket
        global org
        global token
        global url
        global measurement
        global client
        # -----------Parameters send from frontend----------
        myEmail = kwargs['email']
        myPassword = kwargs['password']
        isAuthenticatedByGoogle = kwargs['isAuthenticatedByGoogle']

        if(isAuthenticatedByGoogle == "false"):
            # -----------query for reading data--------
            query_api = client.query_api()    
            query = f'from(bucket:"{databucket}") \
            |> range(start: -1y) \
            |> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}"   and r.password == "{myPassword}"  and r.isAuthenticatedByGoogle == "{isAuthenticatedByGoogle}"  )' 
    
        elif(isAuthenticatedByGoogle == "true"):
            # -----------query for reading data--------
            query_api = client.query_api()    
            query = f'from(bucket:"{databucket}") \
            |> range(start: -1y) \
            |> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}" and r.isAuthenticatedByGoogle == "{isAuthenticatedByGoogle}"  )'
                    
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))

        print(results)
        if(len(results) == 0 ):
            return JsonResponse({"response":"false"},safe=False)
        else:
            return JsonResponse({"response":"true"},safe=False)
    except:
        logger.warning('Error in signing in user '+str(datetime.datetime.now())+' hours!')
