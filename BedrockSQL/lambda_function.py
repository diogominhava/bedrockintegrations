import os
import boto3
import psycopg2
import json
from botocore.exceptions import ClientError
from botocore.config import Config

host = os.environ['DB_HOST']
username = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
port = os.environ['DB_PORT']
database_name = os.environ['DB_DATABASE']
question = os.environ['QUESTION']

boto3_config = Config(
    region_name = 'us-east-1',
    connect_timeout = 5,
    retries = {
        'max_attempts': 3,
        'mode': 'standard'
    }
)
    
try:
    conn = psycopg2.connect(host=host, user=username, password=password, dbname=database_name, port=port, connect_timeout=3)
except psycopg2.Error as e:
    print(e)
    raise

def invoke_claude(question):
        try:
            print("Trying to use Claude")
            client = boto3.client(service_name="bedrock-runtime", config=boto3_config)
            print("Client created")
            prompt = '''
            I have a table in a schema called sales called salesorderdetail. 
            The table has the following columns which are interesting:
                salesorderid: the id of a sales order
                salesorderdetailid: a unique id for the salesorderdetail
                orderqty: a number with the quantity of items ordered
                productid: the product id in the row
                
            Write a SQL query for Postgres to answer the following question:
            ''' + question + "\n return only the SQL query."
            
            
            enclosed_prompt = "Human: " + prompt + "\n\nAssistant:"

            body = {
                "prompt": enclosed_prompt,
                "max_tokens_to_sample": 200,
                "temperature": 0.5,
                "stop_sequences": ["\n\nHuman:"],
            }

            print("Sending request to bedrock")
            
            response = client.invoke_model(
                modelId="anthropic.claude-v2", body=json.dumps(body)
            )

            response_body = json.loads(response["body"].read())
            completion = response_body["completion"]
            print("Got a completion")
            
            return completion

        except ClientError:
            print(ClientError)
            raise
        
def query_database(query):
        try:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return rows
        except psycopg2.Error as e:
            print(e)
            raise

        
def lambda_handler(event, context):
    query = invoke_claude(question)
    print("Query: ")
    print(query)
    results = query_database(query)
    print("================")
    print("Query results: ")
    print(results)
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

# Uncomment to run locally
# lambda_handler("a", "b")