import json
import boto3
import zipfile
from io import BytesIO
src_bucket = 'new-bucket-rlnu'

dest_bucket = 'rlnu-glue-git-example'

def lambda_handler(event, context):
    s3 = boto3.client('s3', use_ssl=False)
    Key_unzip = 'STORE'

    prefix      = "STORE.zip"
    zipped_keys =  s3.list_objects_v2(Bucket=src_bucket, Prefix=prefix, Delimiter = "~")
    file_list = []
    for key in zipped_keys['Contents']:
     file_list.append(key['Key'])
    
    #This will give you list of files in the folder you mentioned as prefix
    s3_resource = boto3.resource('s3')
    
    #Now create zip object one by one, this below is for 1st file in file_list
    zip_obj = s3_resource.Object(bucket_name=src_bucket, key=file_list[0])
    print (zip_obj)
    buffer = BytesIO(zip_obj.get()["Body"].read())

    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        file_info = z.getinfo(filename)
        s3_resource.meta.client.upload_fileobj(
        z.open(filename),
        Bucket=dest_bucket,
        Key='result_files/' + f'{filename}')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


