import json
import boto3
import os
from io import BytesIO
from zipfile import ZipFile
import sys
import traceback
import base64 

### This script is to unzip the large file on ec2 
### prequisite: Need to onetime setup profile, or not to setup trustship
### Will run on super user mode

### Addition steps are added to run the scrip on stop and start

try:
    S3_SORUCE_PATH='s3://new-bucket-rlnu/'
    S3_DESTINATION_PATH='s3://rlnusnowflakeland/unzip_files/'
    ZIP_FILE_NAME='STORE'

    userData = """Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash -ex
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
cd /home/ec2-user/

aws s3 cp ~src_path~~file~.zip ~file~.zip 
unzip -o -q ~file~.zip 
aws s3 cp ~file~.csv ~tgt_root_path~~file~ 
aws s3 mv ~tgt_root_path~~file~ ~tgt_root_path~~file~/~file~.csv
"""

    userData = userData.replace("~file~",ZIP_FILE_NAME).replace("~src_path~",S3_SORUCE_PATH).replace("~tgt_root_path~",S3_DESTINATION_PATH)
    print(userData)
    
    userDataEncoded = base64.b64encode(userData.encode("ascii")).decode("ascii")

    print(userDataEncoded)
    
    client = boto3.client('ec2')
    my_instance = 'i-0240ab086d705dfb6'

    # Stop the instance
    client.stop_instances(InstanceIds=[my_instance])
    waiter=client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[my_instance])

    response = client.modify_instance_attribute(InstanceId=my_instance, UserData={
        'Value': userDataEncoded
    })
    print(response)
    
    #Start Instance here
    res = boto3.resource('ec2')
    ob_my_instance = res.Instance(my_instance)
    ob_my_instance.start()
    ob_my_instance.wait_until_running()

    print('unzipped successful')
except BaseException as ex:
    ex_type, ex_value, ex_traceback = sys.exc_info()
    trace_back = traceback.extract_tb(ex_traceback)
    for trace in trace_back:
        print("Execption occured at Line %d: in %s -> %s funtion for the statement: %s" % (trace[1], trace[0], trace[2], trace[3]))