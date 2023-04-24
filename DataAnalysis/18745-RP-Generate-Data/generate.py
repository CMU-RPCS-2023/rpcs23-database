import random
import json
from datetime import datetime, timedelta
import math

# Set how much simulation file to generate
num_simulations_test = 50
# Set how much simulation data to generate in one file
number_data = 100

gps_default_data =      [
          "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
          "$GPGGA,123520,4807.040,N,01131.001,E,1,08,0.9,545.4,M,46.9,M,,*46",
          "$GPGGA,123521,4807.042,N,01131.003,E,1,08,0.9,545.4,M,46.9,M,,*45",
          "$GPGGA,123522,4807.044,N,01131.006,E,1,08,0.9,545.4,M,46.9,M,,*44",
          "$GPGGA,123523,4807.045,N,01131.010,E,1,08,0.9,545.4,M,46.9,M,,*43",
          "$GPGGA,123524,4807.045,N,01131.015,E,1,08,0.9,545.4,M,46.9,M,,*42",
          "$GPGGA,123525,4807.044,N,01131.020,E,1,08,0.9,545.4,M,46.9,M,,*41",
          "$GPGGA,123526,4807.042,N,01131.024,E,1,08,0.9,545.4,M,46.9,M,,*40",
          "$GPGGA,123527,4807.040,N,01131.027,E,1,08,0.9,545.4,M,46.9,M,,*4F",
          "$GPGGA,123528,4807.038,N,01131.029,E,1,08,0.9,545.4,M,46.9,M,,*4E",
          "$GPGGA,123529,4807.036,N,01131.030,E,1,08,0.9,545.4,M,46.9,M,,*4D",
          "$GPGGA,123530,4807.035,N,01131.030,E,1,08,0.9,545.4,M,46.9,M,,*4C",
          "$GPGGA,123531,4807.033,N,01131.029,E,1,08,0.9,545.4,M,46.9,M,,*4B",
          "$GPGGA,123532,4807.031,N,01131.027,E,1,08,0.9,545.4,M,46.9,M,,*4A",
          "$GPGGA,123533,4807.029,N,01131.024,E,1,08,0.9,545.4,M,46.9,M,,*49",
          "$GPGGA,123534,4807.028,N,01131.020,E,1,08,0.9,545.4,M,46.9,M,,*48",
          "$GPGGA,123535,4807.027,N,01131.015,E,1,08,0.9,545.4,M,46.9,M,,*47",
          "$GPGGA,123536,4807.027,N,01131.010,E,1,08,0.9,545.4,M,46.9,M,,*46",
          "$GPGGA,123537,4807.027,N,01131.006,E,1,08,0.9,545.4,M,46.9,M,,*45",
          "$GPGGA,123538,4807.028,N,01131.003,E,1,08,0.9,545.4,M,46.9,M,,*44",
          "$GPGGA,123539,4807.029,N,01131.001,E,1,08,0.9,545.4,M,46.9,M,,*43",
          "$GPGGA,123540,4807.031,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*42",
          "$GPGGA,123541,4807.033,N,01130.999,E,1,08,0.9,545.4,M,46.9,M,,*41",
          "$GPGGA,123542,4807.035,N,01130.999,E,1,08,0.9,545.4,M,46.9,M,,*40",
          "$GPGGA,123543,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*4F",
          "$GPGGA,123544,4807.040,N,01131.001,E,1,08,0.9,545.4,M,46.9,M,,*4E",
          "$GPGGA,123545,4807.042,N,01131.003,E,1,08,0.9,545.4,M,46.9,M,,*4D",
          "$GPGGA,123546,4807.044,N,01131.006,E,1,08,0.9,545.4,M,46.9,M,,*4C",
          "$GPGGA,123547,4807.045,N,01131.010,E,1,08,0.9,545.4,M,46.9,M,,*4B",
          "$GPGGA,123548,4807.045,N,01131.015,E,1,08,0.9,545.4,M,46.9,M,,*4A",
          "$GPGGA,123549,4807.044,N,01131.020,E,1,08,0.9,545.4,M,46.9,M,,*49",
          "$GPGGA,123550,4807.042,N,01131.024,E,1,08,0.9,545.4,M,46.9,M,,*48",
          "$GPGGA,123551,4807.040,N,01131.027,E,1,08,0.9,545.4,M,46.9,M,,*47",
          "$GPGGA,123552,4807.038,N,01131.029,E,1,08,0.9,545.4,M,46.9,M,,*46",
          "$GPGGA,123553,4807.036,N,01131.030,E,1,08,0.9,545.4,M,46.9,M,,*45",
          "$GPGGA,123554,4807.035,N,01131.030,E,1,08,0.9,545.4,M,46.9,M,,*44",
          "$GPGGA,123555,4807.033,N,01131.029,E,1,08,0.9,545.4,M,46.9,M,,*43",
          "$GPGGA,123556,4807.031,N,01131.027,E,1,08,0.9,545.4,M,46.9,M,,*42",
          "$GPGGA,123557,4807.029,N,01131.024,E,1,08,0.9,545.4,M,46.9,M,,*41",
          "$GPGGA,123558,4807.028,N,01131.020,E,1,08,0.9,545.4,M,46.9,M,,*40",
          "$GPGGA,123559,4807.027,N,01131.015,E,1,08,0.9,545.4,M,46.9,M,,*4F"
      ]

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
    for i in range(num_positions):
        # randomNum = random.randint(0, 20)
        # randomPos = random.randint(0, 10)
        # gps = "$GPGGA,"
        # gps += str(123500 + i)
        # gps += ","
        # gps += "{:.3f}".format(4807 + (randomNum + 25) * 0.001)
        # gps += ",N,0"
        # gps += "{:.3f}".format(11131+ (randomPos) * 0.001)
        # gps += ",E,1,08,0.9,545.4,M,46.9,M,,*46"

        gps_data.append(gps_default_data[i % len(gps_default_data)])
    # print(gps_data)
    return gps_data


def generate_positions(num_points):
    radius = 2
    center_x = 3.5
    center_y = 3.5

    data_points = []
    for i in range(num_points):
        theta = i * (2 * math.pi / num_points)
        x_perturb = random.uniform(-0.1, 0.1)
        y_perturb = random.uniform(-0.1, 0.1)
        r_perturb = random.uniform(-0.1, 0.1)
        x = (radius + r_perturb) * math.cos(theta) + (center_x + x_perturb)
        y = (radius + r_perturb) * math.sin(theta) + (center_y + y_perturb)
        
        # Ensure x and y are within the range of (0,0) and (7,7)
        x = max(0, min(x, 7))
        y = max(0, min(y, 7))
        
        data_points.append({"X": "{:.2f}".format(x), "Y": "{:.2f}".format(y)})

    return data_points

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
    simulation["Position"]["value"] = generate_positions(number_data)
    simulation["Yaw"]["value"] = generate_xyz(number_data)
    simulation["Pitch"]["value"] = generate_xyz(number_data)
    simulation["Roll"]["value"] = generate_xyz(number_data)

    return simulation

import requests
import time

url = 'https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager'

ii = 0
for index in range(num_simulations_test):
    simulation_data = generate_simulation_data(ii)
    print(simulation_data["SimulationId"])
    # Save the data into a JSON file
    # json.dump(simulation_data, outfile, indent=2)
    data = {'operation': 'add_simulation', 'payload': simulation_data}
    response = requests.post(url, data=json.dumps(data))
    print(response.status_code)
    print(response.json())
    if "errorMessage" in response.json().keys():
        print("here")
        ii -= 1
    ii += 1
    time.sleep(4)
