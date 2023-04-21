import random
import json
from datetime import datetime, timedelta

# Set how much simulation file to generate
num_simulations_test = 20
# Set how much simulation data to generate in one file
number_data = 50

simulation_data_template = {
    "SimulationId": "sim0",
    "SimulationName": "Test Simulation Created by Jhao-Ting Chen",
    "StartTime": "2023-03-17T00:52:14",
    "EndTime": "2023-03-18T00:52:14",
    "CarId": "Tesla",
    "TrackId": "easy1",
    "gps": [],
    "Speed": {
        "value": [],
        "time": []
    },
    "CarStatus": {
        "value": [],
        "time": []
    },
    "Accel": {
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
}


# "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
def generate_gps(num_positions):
    # print("called")
    gps_data = []
    randomNum = random.randint(0, 30)
    for i in range(num_positions):
        gps = "$GPGGA,"
        gps += str(123500 + i + randomNum)
        gps += ","
        gps += str(4807 + i * 0.02 + randomNum)
        gps += ",N,"
        gps += str(11131 + i * 0.01 + randomNum)
        gps += ",E,1,08,0.9,545.4,M,46.9,M,,*46"
        gps_data.append(gps)
    # print(gps_data)
    return gps_data


def generate_xyz(num_positions):
    positions = []
    X = round(random.uniform(0, 1), 2)
    Y = round(random.uniform(0, 1), 2)
    Z = round(random.uniform(0, 1), 2)
    for i in range(num_positions):
        position = {
            "X": round(X + i*0.01 + round(random.uniform(-0.05, 0.05), 2), 2),
            "Y": round(Y + i*0.01 + round(random.uniform(-0.05, 0.05), 2), 2),
            "Z": round(Z + i*0.01 + round(random.uniform(-0.05, 0.05), 2), 2),
        }
        positions.append(position)
    return positions


def generate_value(num_value, a, b):
    value = random.randint(a, b)
    values = []
    values.append(value)
    for i in range(num_value - 1):
        # print("generate_value = ", i)
        value = value + random.randint(-2, 2)
        values.append(value)
        # print ("values = ", values)
    return values


def generate_status(status):
    if status <= 0:
        return []
    count = random.randint(2, 5)
    count = min(count, status)
    value = random.randint(0, 1)
    values = []
    for _ in range(count):
        values.append(value)
    return values + generate_status(status - count)


def generate_simulation_data(index):

    simulation = []

    simulation = simulation_data_template.copy()
    simulation["SimulationId"] = f"sim_random_{index}"

    results = generate_gps(number_data)
    simulation["gps"] = results

    simulation["Speed"]["time"] = []
    simulation["CarStatus"]["time"] = []
    simulation["Accel"]["time"] = []
    simulation["Direction"]["time"] = []
    simulation["ServoAngle"]["time"] = []
    simulation["EngineTemperature"]["time"] = []
    simulation["RPM"]["time"] = []
    simulation["Position"]["time"] = []
    simulation["Yaw"]["time"] = []
    simulation["Pitch"]["time"] = []
    simulation["Roll"]["time"] = []

    for j in range(number_data):
        start_time = datetime.strptime(
            simulation["StartTime"], "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.strptime(
            simulation["EndTime"], "%Y-%m-%dT%H:%M:%S")

        time = start_time + \
            timedelta(seconds=random.randint(
                0, int((end_time - start_time).total_seconds())))
        time_str = time.strftime("%Y-%m-%dT%H:%M:%S")

        simulation["Speed"]["time"].append(time_str)
        simulation["CarStatus"]["time"].append(time_str)
        simulation["Accel"]["time"].append(time_str)
        simulation["Direction"]["time"].append(time_str)
        simulation["ServoAngle"]["time"].append(time_str)
        simulation["EngineTemperature"]["time"].append(time_str)
        simulation["RPM"]["time"].append(time_str)
        simulation["Position"]["time"].append(time_str)
        simulation["Yaw"]["time"].append(time_str)
        simulation["Pitch"]["time"].append(time_str)
        simulation["Roll"]["time"].append(time_str)

    simulation["Speed"]["value"] = generate_value(number_data, 0, 100)
    simulation["CarStatus"]["value"] = generate_status(number_data)
    simulation["Accel"]["value"] = generate_value(number_data, -10, 10)
    simulation["Direction"]["value"] = generate_value(number_data, -10, 10)
    simulation["ServoAngle"]["value"] = generate_value(number_data, -10, 10)
    simulation["EngineTemperature"]["value"] = generate_value(
        number_data, -15, 15)
    simulation["RPM"]["value"] = generate_value(number_data, -10, 10)
    simulation["Position"]["value"] = generate_xyz(number_data)
    simulation["Yaw"]["value"] = generate_xyz(number_data)
    simulation["Pitch"]["value"] = generate_xyz(number_data)
    simulation["Roll"]["value"] = generate_xyz(number_data)

    return simulation

import requests

url = 'https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager'

for index in range(num_simulations_test):
    simulation_data = generate_simulation_data(index)
    # Save the data into a JSON file
    # json.dump(simulation_data, outfile, indent=2)
    data = {'operation': 'add_simulation', 'payload': simulation_data}
    response = requests.post(url, data=json.dumps(data))
    print(response.status_code)
    print(response.json())
