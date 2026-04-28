import json, boto3, uuid, time

# 1. Explicitly set the region to match your DynamoDB table
REGION = 'ap-south-1' 
db = boto3.resource('dynamodb', region_name=REGION)

# 2. Match the name EXACTLY (case-sensitive)
TABLE_NAME = 'Orders' 
table = db.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        # Extract body safely
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        # Database write
        order_id = str(uuid.uuid4())
        table.put_item(Item={
            'order_id': order_id,
            'sku': body.get('sku', 'TEST_ITEM'),
            'qty': body.get('qty', 0),
            'timestamp': int(time.time())
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'success', 'order_id': order_id})
        }
    except Exception as e:
        # This will return the EXACT error to your PowerShell
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed at table '{TABLE_NAME}' in {REGION}: {str(e)}"})
        }