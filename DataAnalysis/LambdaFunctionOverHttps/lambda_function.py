import boto3
import json
import copy

# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

EVENT_TEMPLATE = {
    "Timestamp": "None",
    "EventType": "None",
    "Risk": "None",
    "ErrorMessage": "None"
}

SENSOR_TEMPLATE = {
    "Timestamp": "None",
    "SensorType": "None",
    "Value": "None"
}

CARLOG_TEMPLATE = {
    "Timestamp": "None",
    "CarStatus": "None",
    "Speed": "None",
    "Position": {
        "x": "None",
        "y": "None",
        "z": "None"
    },
    "Yaw": {
        "x": "None",
        "y": "None",
        "z": "None"
    },
    "Pitch": {
        "x": "None",
        "y": "None",
        "z": "None"
    },
    "Roll": {
        "x": "None",
        "y": "None",
        "z": "None"
    },
    "Accel": {
        "x": "None",
        "y": "None",
        "z": "None"
    },
    "Direction": "None",
    "ServoAngle": "None",
    "EngineTemperature": "None",
    "RPM": "None"
}

SIMULATION_TEMPLATE = {
    "SimulationName": "None",
    "SimulationId": "None",
    "StartTime": "None",
    "EndTime": "None",
    "CarId": "None",
    "TrackId": "None",
    "EventLog": [],
    "CarLog": [],
    "SensorLog": []
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
        return {"Object": res, "HTTPStatusCode": status}

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

    def getDefaultEvent(payload):
        res = copy.deepcopy(EVENT_TEMPLATE)

        entries = payload.keys()
        fixed_entries = res.keys()
        entries = [entry for entry in entries if entry in fixed_entries]

        for entry in entries:
            res[entry] = str(payload[entry])
        
        return res

    def getDefaultCarLog(payload):
        res = copy.deepcopy(CARLOG_TEMPLATE)

        FLOAT3 = ["Position", "Yaw", "Pitch", "Roll", "Accel"]
        entries = payload.keys()
        fixed_entries = res.keys()
        entries = [entry for entry in entries if entry in fixed_entries]

        for entry in entries:
            if entry in FLOAT3:
                for axis in [k for k in payload[entry].keys() if k in ["x", "y", "z"]]:
                    res[entry][axis] = str(payload[entry][axis])
            else:
                res[entry] = str(payload[entry])

        return res

    def getDefaultSensorLog(payload):
        res = copy.deepcopy(SENSOR_TEMPLATE)

        entries = payload.keys()
        fixed_entries = res.keys()
        entries = [entry for entry in entries if entry in fixed_entries]

        for entry in entries:
            res[entry] = str(payload[entry])
        
        return res

    def getDefaultSimulation(payload):
        res = copy.deepcopy(SIMULATION_TEMPLATE)

        entries = payload.keys()
        fixed_entries = res.keys()
        filtered_entries = [entry for entry in entries if entry in fixed_entries]

        for entry in filtered_entries:
            if entry == "SimulationId":
                res[entry] = payload[entry]
                res["id"] = payload["SimulationId"]
            elif entry == "EventLog":
                for events in payload[entry]:
                    res[entry].append(getDefaultEvent(events))
            elif entry == "CarLog":
                for events in payload[entry]:
                    res[entry].append(getDefaultCarLog(events))
            elif entry == "SensorLog":
                for events in payload[entry]:
                    res[entry].append(getDefaultSensorLog(events))
            else:
                res[entry] = str(payload[entry])
        return res

    def addSimulation(payload):
        simulation = {
            "Item": getDefaultSimulation(payload)
        }
        return ddb_create(simulation)

    def getSimulation(payload):
        simulation = {
            "Key": {
                "id": str(payload['SimulationId'])
            }
        }
        return filter_data(ddb_read(simulation), [] if 'content' not in payload.keys() else payload['content'])

    def deleteSimulation(payload):
        simulation = {
            "Key": {
                "id": str(payload['SimulationId'])
            }
        }
        return ddb_delete(simulation)

    # define the functions used to return data for plotting
    def filter_data(result, content):
        if len(content) == 0: return result
        if "Item" not in result["Object"].keys():
            return result
        all_data_requested = {}
        all_data_requested["HTTPStatusCode"] = result["HTTPStatusCode"]
        result = result["Object"]["Item"]

        for k in result.keys():
            if k not in ["EventLog", "CarLog", "SensorLog"]:
                all_data_requested[k] = result[k]

        def getFilteredCarLog(k):
            l = {}
            l['value'] = [data[k] for data in result["CarLog"]]
            l['time'] = [data["Timestamp"] for data in result["CarLog"]]
            return l

        for entry in ["Speed", "Position", "Direction", "Yaw", "Pitch", "Roll", "Accel", "ServoAngle", "CarStatus", "EngineTemperature", "RPM"]:
            if entry in content:
                all_data_requested[entry] = getFilteredCarLog(entry)

        if "Sensor" in content:
            all_data_requested[entry] = result["SensorLog"]

        if "Event" in content:
            all_data_requested[entry] = result["EventLog"]

        return all_data_requested

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