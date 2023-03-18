# rapid-test

# cmu-18745
18-745: Rapid Prototyping of Computer Systems

### Usage:
1. Get Filtered Data for HCI team:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "get_simulation", "payload": {"SimulationId": "ExampleGraphTest", "content": ["Speed", "ServoAngle", "Accel"]}}'
    ```
2. create:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "create", "payload": {"Item": {"id": "TestCreate1", "number": 1234}}}'
    ```
3. read:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "read", "payload": {"Key": {"id": "TestCreate1"}}}'
    ```
4. update:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "update", "payload": {"Key": {"id": "TestCreate1"}, "AttributeUpdates": {"number": {"Value": [{"test1": "val1", "key2": "val2"}]}}}}'
    ```
5. delete
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "delete", "payload": {"Key": {"id": "TestCreate1"}}}'
    ```
6. add_simulation:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "add_simulation", "payload": {"SimulationId": 1}}'
    ```
7. get_simulation:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "get_simulation", "payload": {"SimulationId": 1}}'
    ```
8. delete_simulation:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "delete_simulation", "payload": {"SimulationId": 1}}'
    ```


### Data:

|  <div style="width:180px">Team</div> | <div style="width:130px">Data Key</div>      | <div style="width:180px">Format</div> | Explanation |
| ------------------- | ----------------- | ------------- | ---------------|
|  General               | CarID      | String  | The car type ID |
|                     | ID         | String | The customer ID | 
|                     | TrackID         | String | The track type ID | 
| SW Ground Systems   | Position          | Float - (x, y, z) | The location of the vehicle | 
|                     | Direction         | Float - (dir, t) | The orientation of the vehicle going forward | 
| SW Vehicle Controls | Yaw               | Float - (x, y, z) | The rotation of the vehicle around its vertical axis | 
|                     | Pitch             | Float - (x, y, z) | The rotational movement of the vehicle around its side-to-side axis | 
|                     | Roll  | Float - (x, y, z) | The rotation of the vehicle around its longitudinal axis |
|                     | Accel  | Float - (x, y, z) | The rate of change of velocity over time (Acceleration) |
|                     | Servo angle  | Int | The rotational position of a servo motor's output shaft |
|                     | Speed  | Int | How fast an object is moving (distance traveled per unit of time) |
| Others              | CarStatus | String | on/off |
|                     | Engine Temperature | Int | The temperature of the vehicle's engine |
|                     | RPM | Int | The rotational speed of a mechanical component (Revolutions per minute) |
|                     | Risk | Int | The probability or likelihood of harm, injury, damage, loss, or negative consequences |
|                     | Error Message | String | The content of error |
|                     | Event Type | Int | The type of event |
