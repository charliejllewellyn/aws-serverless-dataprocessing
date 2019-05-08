import boto3
import json
import random
import requests
import uuid
num = str(random.randint(1,101))
s3 = boto3.client('s3')

r = s3.select_object_content(
        Bucket='cjl-temp-dub',
        Key='training_images/fall11_urls.txt',
        ExpressionType='SQL',
        Expression="select * from s3object s where s._1 like '%" + num + "%' and s._2 like '%jpg%' limit 100",
        InputSerialization = {'CSV': {"FileHeaderInfo": "Ignore"}},
        OutputSerialization = {'JSON': {}},
)
#Expression="select * from s3object s where s._1 like '%01% limit 10'",

def getObject(url):
    return requests.get(url)

def uploadImage():
    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            for line in records.splitlines():
                jsonData = json.loads(line)
                print(jsonData['_2'])
                try:
                    response = getObject(jsonData['_2'])
                    filename = str(uuid.uuid4())
                    open('/tmp/' + str(filename), 'wb').write(response.content)
                    s3.upload_file('/tmp/' + filename,'serverlessdataprocessing-application-inputbucket-1giiap2ip6qwt',filename,ExtraArgs={'ContentType': "image/jpeg"})
                    return
                except Exception as e:
                    print(e)
                    continue
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']
            print("Stats details bytesScanned: ")

uploadImage()
