import uuid
import boto3

AWSKEY = 'AKIARXFY66LJUCFEMVXS'
AWSSECRET = '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'

def get_table(name):
    dbclient = boto3.resource(service_name= 'dynamodb',
                          region_name='us-east-1',
                          aws_access_key_id=AWSKEY,
                          aws_secret_access_key=AWSSECRET)
    return dbclient.Table(name)


def add_post(UserName, Text, Date, ParentID=''):
    PostID = str(uuid.uuid4())
    post={'PostID':PostID,
          'ParentID':ParentID,
          'UserName': UserName,
          'Text':Text,
          'Date': Date}
    table = get_table('Post')
    table.put_item(Item=post)

def delete_post(PostID):
    table = get_table('Post')
    table.delete_item(Key={'PostID':PostID})

def get_post(PostID):
    table = get_table('Post')
    result = table.get_item(Key={'PostID' :PostID})
    if 'Item' not in result:
        return None
    return result['Item']

def post_items():
    table= get_table('Post')
    results= []
    for item in table.scan()['Items']:
        if item.get('ParentID', '') == '':
            results.append(item)

    results.sort(key=lambda d: d['Date'], reverse=True)
    return results

def loadpostsbyusername(UserName):
    table = get_table('Post')
    results = []
    for item in table.scan()['Items']:
        if item['UserName'] == UserName and item['ParentID'] == '':
            results.append(item)
    results = sorted(results, key=lambda x: x['Date'], reverse=True)
    return results

def listfeed():
    table = get_table('Post')
    results = []
    for item in table.scan()['Items']:
        if item['ParentID'] == '':
            results.append(item)
    results = sorted(results, key=lambda x: x['Date'], reverse=True)
    return results


def loadreplies(PostID):
    table = get_table('Post')
    results = []
    for item in table.scan()['Items']:
        if item['ParentID'] == PostID:
            results.append(item)
    results = sorted(results, key=lambda x: x['Date'])
    return results

def add_user(email, UserName, Password):
    user={'email': email,
          'UserName':UserName,
          'Password':Password,
          'ProfilePic':'generic.png'
          }
    table = get_table('Users')
    table.put_item(Item=user)

def list_items():
    table= get_table('Users')
    results= []
    for item in table.scan()['Items']:
        results.append(item)
    return results

def find_username(username):
    table= get_table('Users')
    for item in table.scan()['Items']:
        if 'UserName' not in item: continue
        if item['UserName'] == username: return item
    return None

def find_user(email):
    table = get_table('Users')
    result= table.get_item(Key={'email':email})
    if 'Item' not in result:
        return None
    return result['Item']

def update_user_pic(email, ProfilePic):
    table = get_table('Users')
    table.update_item(
        Key={'email':email},
        UpdateExpression='set ProfilePic= :r',
        ExpressionAttributeValues={':r':ProfilePic}
    )

def add_remember_key(email):
    table = get_table('Remember')
    key = str(uuid.uuid4()) + str(uuid.uuid4())
    item = {'key':key, 'email':email}
    table.put_item(Item=item)
    return key

def add_image():
    ImageID = str(uuid.uuid4())
    image={'ImageID':ImageID}
    table = get_table('Images')
    table.put_item(Item=image)

def image_items():
    table= get_table('Images')
    results= []
    for item in table.scan()['Items']:
        results.append(item)
    return results