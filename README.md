# cmu-18745
18-745: Rapid Prototyping of Computer Systems

### Usage:
1. create:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "create", "payload": {"Item": {"id": "TestCreate1", "number": 1234}}}'
    ```
2. read:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "read", "payload": {"Key": {"id": "TestCreate1"}}}'
    ```
3. update:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "update", "payload": {"Key": {"id": "TestCreate1"}, "AttributeUpdates": {"number": {"Value": [{"test1": "val1", "key2": "val2"}]}}}}'
    ```
4. delete
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "delete", "payload": {"Key": {"id": "TestCreate1"}}}'
    ```
5. add_simulation:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "add_simulation", "payload": {"SimulationId": 1}}'
    ```
6. get_simulation:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "get_simulation", "payload": {"SimulationId": 1}}'
    ```
7. delete_simulation:
    ```
    curl -X POST https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager -d '{"operation": "delete_simulation", "payload": {"SimulationId": 1}}'
    ```