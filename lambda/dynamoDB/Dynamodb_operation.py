import json
import boto3
import dynamo_config

class dynamodb_operation():

    # Override the json method
    def load_json(self,path):
        try:
            with open(path) as json_file:
                data = json.load(json_file)
        except Exception as e:
            print('ERROR: no such file like ' + path)
            exit(-1)
        else:
            return data

    # Constructor connect to DB
    def __init__(self):
        # conf = self.load_json(path)
        self.client = boto3.client('dynamodb',region_name=dynamo_config.region_name,aws_access_key_id=dynamo_config.aws_access_key_id, aws_secret_access_key=dynamo_config.aws_secret_access_key)

    # List all tables in dynamoDB
    def list_all_table(self):
        page = 1
        LastEvaluationTableName = ""
        while True:
            if page == 1:
                response = self.client.list_tables()
            else:
                response = self.client.list_tables(
                    ExclusiveStartTableName=LastEvaluationTableName
                )

            TableNames = response['TableNames']
            for table in TableNames:
                print(table)
            if 'LastEvaluatedTableName' in response:
                LastEvaluationTableName = response["LastEvaluatedTableName"]
            else:
                break
            page += 1

    # Get information about a table
    def get_table_desc_only(self,table):
        try:
            response = self.client.describe_table(TableName=table)
        except Exception as e:
            print('ERROR: no such table like ' + table)
            exit(-1)
        else:
            return response["Table"]

    # Get table size
    def get_table_size(self,table):
        response = self.get_table_desc_only(table)
        stastic = {}
        stastic['TableSizeBytes'] = response['TableSizeBytes']
        stastic['ItemCount'] = response['ItemCount']
        return stastic

    # Create table
    def create_table(self,tablename,keySchema,attributeDefinitions,provisionedThroughput):
        table = self.client.create_table(
            TableName=tablename,
            KeySchema=keySchema,
            AttributeDefinitions=attributeDefinitions,
            ProvisionedThroughput=provisionedThroughput
        )

        # Wait until the table exists.
        self.client.get_waiter('table_exists').wait(TableName=tablename)

        response = self.client.describe_table(TableName=tablename)
        print(response)

    # Insert data
    def put_item(self,tableName,item):
        try:
            self.client.put_item(
                TableName=tableName,
                Item=item
            )
        except Exception as e:
            print('ERROR: put item fail. msg: ' + str(e))
            exit(-1)
        else:
            return 'Success'

    # Delete table
    def delete_table(self,table):
        try:
            self.client.delete_table(
                TableName=table
            )
        except Exception as e:
            print('ERROR: delete table ' + table + ' fail. msg: ' + str(e))
        else:
            print('delete table ' + table + ' success')
