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

# --------------Posting the data in influxdb-----------
@csrf_exempt
def postUserData(request):
    logger.warning('Attemp to post user data '+str(datetime.datetime.now())+' hours!')
    try:
        # ----------Using global variable---------
        global bucket
        global org
        global token
        global url
        global measurement
        global client
        # -----------Parameters send from frontend----------
        data = json.loads(request.body)
        myUsername = data.get('myUsername')
        myEmail = data.get('myEmail')
        myPassword = data.get('myPassword')
        isAuthenticatedByGoogle = data.get('isAuthenticatedByGoogle')

        # ----------Query for checking whether user with same email exist--------
        query_api = client.query_api()
        query = f'from(bucket:"{databucket}")|> range(start: -1y)|> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}" )'
        # ----------append data in array-----------
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))
        # --------checking wether user with same email exist or not---------- 
        if(len(results) == 0 ):
            # ----------code for posting data----------
            # Define the data to be written
            data = Point(measurement).tag("isAuthenticatedByGoogle", isAuthenticatedByGoogle).field("username", myUsername).tag("email",myEmail).tag("password", myPassword).time(datetime.datetime.utcnow().isoformat() + 'Z')
            # Create a write API instance
            write_api = client.write_api(write_options=SYNCHRONOUS)
            # Write the data to the bucket
            write_api.write(bucket=databucket, record=data)
            # Close the write API
            write_api.close()
            print("--------------user registered successfully------------")
            response = json.dumps(data, default=str)
            return JsonResponse(response,safe=False)
        print("--------------Already Exist User------------")
        return JsonResponse({"response":"Already Exist User"},safe=False)
    except:
        logger.warning('Error in posting users data'+str(datetime.datetime.now())+' hours!')
