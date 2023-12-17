
import datetime
import time
import threading
import schedule
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from smartNursingBackend.settings import logger

def firstThread():
    def job():

        

        global newLogFileNamesArray
        newLogFileNamesArray = readDataFromFile('logFileNames.txt')
        if(len(newLogFileNamesArray) != 0):
            for i in range(len(newLogFileNamesArray)):
                print("logs\{}".format(newLogFileNamesArray[i]))
                infile = r"logs\{}".format(newLogFileNamesArray[i])
                with open(infile) as f:
                    f = f.readlines()
                logsArray=[]
                for index, item in enumerate(f):
                    logsArray.append(item)
                    print(item)
                    postData(item)
                print(logsArray)
            deleteDataFromFile('logFileNames.txt')
    schedule.every().day.at("00:02").do(job)

    # ---------global variables accessing in fumction---------    
    global newLogFileNamesArray
    directory = 'logs'
    initial_files = os.listdir(directory)

    while True:
        schedule.run_pending()
        time.sleep(1)
        updated_files = os.listdir(directory)
        new_files = list(set(updated_files) - set(initial_files))
        if new_files:
            for file in new_files:
                print(f"New file generated: {file}")
                writeDataToFile('logFileNames.txt',file)
        initial_files = updated_files

def postData(logsData):
    logger.warning("Attempt to post logs in influxdb cloud" + str(datetime.datetime.now())+' hours!')
    try:
        global client
        # Define the data to be written
        data = Point("logs").field("logs",logsData).time(datetime.datetime.utcnow().isoformat() + 'Z')
        # Create a write API instance
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # Write the data to the bucket
        write_api.write(bucket="Logs", record=data)
        # Close the write API
        write_api.close()
    except:
        logger.warning("Failed to post logs in influxdb cloud" + str(datetime.datetime.now())+' hours!')

def writeDataToFile(fileName,data):
    logger.warning("Attempt to writing data in logFileNames.txt file" + str(datetime.datetime.now())+' hours!')
    try:
        with open(fileName, 'a') as f:
            f.write(data)
            f.write('\n')
    except:
        logger.warning("Failed to write data in logFileNames.txt file" + str(datetime.datetime.now())+' hours!')

def readDataFromFile(fileName):
    logger.warning("Attempt to reading data from logFileNames.txt file" + str(datetime.datetime.now())+' hours!')
    try:
        file = open(fileName, 'r')
        array=[]
        while True:
            line = file.readline()
            if not line:
                break
            array.append(line[:-1])
        return array
        file.close()
    except:
        logger.warning("Failed to read data from logFileNames.txt file" + str(datetime.datetime.now())+' hours!')

def deleteDataFromFile(fileName):
    logger.warning("Attempt to delete data from logFileNames.txt file" + str(datetime.datetime.now())+' hours!')
    try:
        open(fileName , 'w').close()
    except:
        logger.warning("Failed to delete data from logFileNames.txt file" + str(datetime.datetime.now())+' hours!')


# Create a thread object with your function
myThread1 = threading.Thread(target=firstThread,daemon=True)








