import boto3
import copy
import numpy as np
from datetime import datetime

# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

DATE_EXPECTED_FORMAT = "%Y-%m-%dT%H:%M:%S"

DB_ACCEPT_TYPES = [
    int,
    str
]

STRING_ENTRIES = [
    "SimulationName",
    "SimulationId",
    "StartTime",
    "EndTime",
    "CarId",
    "TrackId",
]

LIST_ENTRIES = [
    "gps"
]

ENTRY_EXPECTED_TYPES = {
    "Speed": int,
    "Accel": int,
    "CarStatus": int,
    "Position": dict,
    "Yaw": dict,
    "Pitch": dict,
    "Roll": dict,
    "Direction": int,
    "ServoAngle": int,
    "EngineTemperature": None,
    "RPM": int
}

SIMULATION_TEMPLATE = {
    "SimulationName": "None",
    "SimulationId": "None",
    "StartTime": "None",
    "EndTime": "None",
    "CarId": "None",
    "TrackId": "None",
    "gps": [],
    "Speed": {
        "value": [],
        "time": []
    },
    "Accel": {
        "value": [],
        "time": []
    },
    "CarStatus": {
        "value": [],
        "time": []
    },
    "Position": {
        "value": [],
        "time": []
    },
    "Yaw": {
        "value": [],
        "time": []
    },
    "Pitch": {
        "value": [],
        "time": []
    },
    "Roll": {
        "value": [],
        "time": []
    },
    "Direction": {
        "value": [],
        "time": []
    },
    "ServoAngle": {
        "value": [],
        "time": []
    },
    "EngineTemperature": {
        "value": [],
        "time": []
    },
    "RPM": {
        "value": [],
        "time": []
    },
}

ENTRY_TEMPLATE = {
    "value": [],
    "time": []
}

def checkEntry(entry_name, payload):
    if entry_name in STRING_ENTRIES:
        return True, str(payload)
    if entry_name in LIST_ENTRIES:
        try:
            return True, [str(p) for p in payload]
        except:
            return False, f'entry {entry_name} should be a list of strings, instead it got {payload}'
    else:
        try:
            values = payload['value']
            times = payload['time']
            if (len(values) != len(times)):
                return False, f'entry {entry_name} has different lengths of data.'
            
            if (len(values) == 0):
                return_value = {
                    "value": values,
                    "time": times
                }
                return True, return_value
            
            try:
                expected_type = ENTRY_EXPECTED_TYPES[entry_name]
            except:
                expected_type = None
            if expected_type is None:
                t = type(values[0])
                if t in DB_ACCEPT_TYPES:
                    bad_vals = [type(v) for v in values if type(v) != t]
                    if len(bad_vals) > 0:
                        values = [str(v) for v in values]
                else:
                    values = [str(v) for v in values]
            else:
                bad_vals = [type(v) for v in values if type(v) != expected_type]
                if len(bad_vals) > 0:
                    return False, f'entry {entry_name} expects type {expected_type}.'
                if expected_type is dict:
                    new_values = []
                    for value in values:
                        new_value = {}
                        for k, v in value.items():
                            new_value[str(k)] = str(v)
                        new_values.append(new_value)
                    values = new_values

            for t in times:
                try:
                    datetime.strptime(str(t), DATE_EXPECTED_FORMAT)
                except:
                    return False, f'entry {entry_name} has time string format error. Expected: {DATE_EXPECTED_FORMAT}, Got: {t}'

            return_value = {
                "value": values,
                "time": times
            }

            return True, return_value
        except:
            return False, f'entry {entry_name} does not have "value" and "time" as dictionary keys'


def getDefaultSimulation(payload):
    res = copy.deepcopy(SIMULATION_TEMPLATE)

    entries = payload.keys()
    fixed_entries = res.keys()
    filtered_entries = [entry for entry in entries if entry in fixed_entries]

    if "SimulationId" not in filtered_entries:
        return False, f'"SimulationId" not provided, cannot create a new simulation.'

    for entry in filtered_entries:
        if entry == "SimulationId":
            res[entry] = payload[entry]
            res["id"] = payload["SimulationId"]
        else:
            success, value = checkEntry(entry, payload[entry], )
            if success:
                res[entry] = value
            else:
                return False,  f'entry {entry} error: {value}'
    return True, res


def anomaly_detector(orig_data):
    try:
        data_list = orig_data['value']
        time_list = orig_data['time']
        
        window_size = 10
        window = []
        threshold = 2
        anomaly = []

        for i, data in enumerate(data_list):
            window.append(data)
            if (len(window) == window_size):
                mean = np.mean(window)
                std = np.std(window)
                z_score = (data - mean) / std
                if abs(z_score) > threshold:
                    # anomaly.append({
                    #     "value": data,
                    #     "time": time_list[i],
                    #     "index": i,
                    #     "confidence": z_score})
                    anomaly.append(i)
                window.pop(0)

        orig_data['anomaly'] = anomaly
    except:
        pass
    return orig_data


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
    
    def searchId(x):
        response = dynamo.scan(ProjectionExpression="SimulationId")
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = dynamo.scan(ExclusiveStartKey=response['LastEvaluatedKey'], ProjectionExpression="SimulationId")
            items.extend(response['Items'])

        ids = [item['SimulationId'] for item in items if len(item.keys())]
        returned_message = {}
        returned_message["IDs"] = ids
        returned_message["HTTPStatusCode"] = 200
        returned_message["Message"] = "Success"
        return returned_message

    operation = event['operation']


    def addSimulation(payload):
        success, simulation = getDefaultSimulation(payload)
        if success:
            simulation = {
                "Item": simulation
            }
            returned_message = ddb_create(simulation)
            if returned_message["HTTPStatusCode"] == 200:
                returned_message["Message"] = "Success"
            return returned_message
        else:
            returned_message = {}
            returned_message["HTTPStatusCode"] = 400
            returned_message["ErrorMessage"] = simulation
            return returned_message

    def getSimulation(payload):
        try:
            simulation = {
                "Key": {
                    "id": str(payload['SimulationId'])
                }
            }
            return filter_data(ddb_read(simulation), [] if 'content' not in payload.keys() else payload['content'], False if 'anomalyDetection' not in payload.keys() else payload['anomalyDetection'])
        except:
            returned_message = {}
            returned_message["HTTPStatusCode"] = 400
            returned_message["ErrorMessage"] = "Expected to have \"SimulationId\""
            return returned_message

    def deleteSimulation(payload):
        try:
            simulation = {
                "Key": {
                    "id": str(payload['SimulationId'])
                }
            }
            returned_message = ddb_delete(simulation)
            if returned_message["HTTPStatusCode"] == 200:
                returned_message["Message"] = "Success"
            return returned_message
        except:
            returned_message = {}
            returned_message["HTTPStatusCode"] = 400
            returned_message["ErrorMessage"] = "Expected to have \"SimulationId\""
            return returned_message

    # define the functions used to return data for plotting
    def filter_data(result, content = [], anomaly_detection = False):
        if "Item" not in result["Object"].keys():
            result["ErrorMessage"] = "Simulation not found. Check SimulationId again."
            return result
        all_data_requested = {}
        all_data_requested["HTTPStatusCode"] = result["HTTPStatusCode"]
        result = result["Object"]["Item"]

        if len(content) == 0: 
            for k, v in result.items():
                try:
                    if anomaly_detection:
                        all_data_requested[k] = anomaly_detector(v)
                    else:
                        all_data_requested[k] = v
                except:
                    all_data_requested[k] = v
            return all_data_requested
        else:
            for entry in content:
                try:
                    if anomaly_detection:
                        all_data_requested[entry] = anomaly_detector(result[entry])
                    else:
                        all_data_requested[entry] = result[entry]
                except:
                    all_data_requested = {}
                    all_data_requested["HTTPStatusCode"] = 400
                    all_data_requested["ErrorMessage"] = f'Item does not contain entry: {entry}, see "Item" for more details.'
                    all_data_requested["Item"] = result
                    return all_data_requested

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
        "search_ids": searchId,
    }

    if operation in operations:
        return operations[operation](event.get('payload'))
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))