import boto3


def get_content(auth, bucket, key):
    try:
        s3 = boto3.resource('s3',
                            region_name=auth['region'],
                            aws_access_key_id=auth['aws_access_key_id'],
                            aws_secret_access_key=auth['aws_secret_access_key']
                            )

        obj = s3.Object(bucket, key)
        return obj.get()['Body'].read().decode('utf-8')
    except Exception as e:
        print('{}'.format(e))
        raise


def s3_write(auth, bucket, key, content):
    try:
        s3 = boto3.resource('s3',
                            region_name=auth['region'],
                            aws_access_key_id=auth['aws_access_key_id'],
                            aws_secret_access_key=auth['aws_secret_access_key']
                            )

        obj = s3.Object(bucket, key).put(Body=content)
    except Exception as e:
        print('{}'.format(e))
        raise


def get_files(bucket, key):
    pass
