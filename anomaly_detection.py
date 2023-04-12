import numpy as np

def anomaly_detector(orig_data, attribute):
    data_list = []
    for carlog in orig_data['CarLog']:
        data = carlog[attribute]
        data_list.append(data)
    
    window_size = 10
    window = []
    threshold = 2
    anomaly = []

    for data in data_list:
        window.append(data)
        if (len(window) == window_size):
            mean = np.mean(window)
            std = np.std(window)
            z_score = (data - mean) / std
            if abs(z_score) > threshold:
                # print("Anomaly Detected: {}".format(speed))
                anomaly.append((1, z_score))
            else:
                anomaly.append((0, z_score))
            window.pop(0)
        else:
            anomaly.append((0, None))

    orig_data['Anomaly'] = anomaly

    return orig_data