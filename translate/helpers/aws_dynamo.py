import boto3


class AWSDynamo:
    def __init__(self, auth, table_name):
        self.dynamodb = boto3.resource('dynamodb',
                                       region_name=auth['region'],
                                       aws_access_key_id=auth['aws_access_key_id'],
                                       aws_secret_access_key=auth['aws_secret_access_key']
                                       )
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)

    def delete(self, key):
        self.table.delete_item(Key=key)

    def put(self, item):
        try:
            self.table.put_item(Item=item)
        except Exception as e:
            print('Exception inserting {}'.format(e))
            raise

    def get(self, key):
        try:
            response = self.table.get_item(TableName=self.table_name, Key=key)
            return response.get('Item')
        except Exception as e:
            print('Exception getting {}'.format(e))
            raise
