import boto3

AWSKEY = 'AKIARXFY66LJUCFEMVXS'
AWSSECRET = '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'
PUBLIC_BUCKET = 'kblackwood-web-public'
STORAGE_URL = 'https://s3.amazonaws.com/' + PUBLIC_BUCKET + '/'

def get_public_bucket():
    s3client = boto3.resource(service_name = 's3',
                          region_name='us-east-1',
                          aws_access_key_id=AWSKEY,
                          aws_secret_access_key=AWSSECRET)

    bucket = s3client.Bucket(PUBLIC_BUCKET)

    return bucket

def listfiles():
    bucket = get_public_bucket()
    items =[]
    for item in bucket.objects.all():
        items.append(item.key)

    return {'url':STORAGE_URL,'items':items }