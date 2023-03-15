import boto3
import json

# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

EVENT_TEMPLATE = {
    "Timestamp": "2023-03-14T01:03:04",
    "EventType": "Collision",
    "Risk": 3,
    "ErrorMessage": "Hit a tree"
}

CARLOG_TEMPLATE = {
    "Timestamp": "2023-03-14T01:03:04",
    "Speed": 30,
    "Location": {
        "X": "4.2",
        "Y": "2.3"
    },
    "EngineTemperature": 60,
    "RPM": 3
}

SIMULATION_TEMPLATE = {
    "SimulationName": "Sim_1",
    "SimulationId": -1,
    "StartTime": "2023-03-14T01:02:03",
    "EndTime": "2023-03-14T04:05:06",
    "CarId": -1,
    "TrackId": -1,
    "EventLog": [],
    "CarLog": []
}

def lambda_handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
                 operation being performed
    '''

    # define the functions used to perform the CRUD operations
    def ddb_create(x):
        res = dynamo.put_item(**x)
        status = res["ResponseMetadata"]["HTTPStatusCode"]
        return {"HTTPStatusCode": status}
    
    def ddb_read(x):
        # {"operation": "update","payload": {"Key": {"id": "1234ABCD"}}}}
        res = dynamo.get_item(**x)
        status = res["ResponseMetadata"]["HTTPStatusCode"]
        return {"Item": res["Item"], "HTTPStatusCode": status}

    def ddb_update(x):
        # {"operation": "update","payload": {"Key": {"id": "1234ABCD"},"AttributeUpdates": {"number": {"Value": 10}}}}
        res = dynamo.update_item(**x)
        status = res["ResponseMetadata"]["HTTPStatusCode"]
        return {"HTTPStatusCode": status}
        
    def ddb_delete(x):
        # '{"operation": "delete", "payload": {"Key": {"id": "xxx"}}}'
        res = dynamo.delete_item(**x)
        status = res["ResponseMetadata"]["HTTPStatusCode"]
        return {"HTTPStatusCode": status}

    def echo(x):
        return x

    operation = event['operation']

    def getDefaultEvent():
        res = EVENT_TEMPLATE
        return res

    def getDefaultCarLog():
        res = CARLOG_TEMPLATE
        return res

    def getDefaultSimulation(simId):
        res = SIMULATION_TEMPLATE
        res["SimulationId"] = simId
        res["EventLog"].append(getDefaultEvent())
        res["CarLog"].append(getDefaultCarLog())
        res["id"] = str(simId)
        return res

    def addSimulation(payload):
        simulation = {
            "Item": getDefaultSimulation(payload['SimulationId'])
        }
        return ddb_create(simulation)

    def getSimulation(payload):
        simulation = {
            "Key": {
                "id": str(payload['SimulationId'])
            }
        }
        return ddb_read(simulation)

    def deleteSimulation(payload):
        simulation = {
            "Key": {
                "id": str(payload['SimulationId'])
            }
        }
        return ddb_delete(simulation)

    operations = {
        'create': ddb_create,
        'read': ddb_read,
        'update': ddb_update,
        'delete': ddb_delete,
        'echo': echo,
        "add_simulation": addSimulation,
        "get_simulation": getSimulation,
        "delete_simulation": deleteSimulation,
    }

    if operation in operations:
        return operations[operation](event.get('payload'))
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))