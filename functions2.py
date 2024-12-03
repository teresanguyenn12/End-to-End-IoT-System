import config.mongo as mongo
from datetime import datetime, timedelta
from pprint import pprint
import json

# Function to read JSON data from a file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def compute_avg_moisture() -> str:
    '''
        Get average refrigerator moisture data within the past 3 hours
    '''
    data = mongo.get_refrigerator_data()
    current_time = datetime.now()

    # Compute the time 3 hours ago
    three_hours_ago = current_time - timedelta(hours=3)

    # Load device data from the boards.json file
    device_data = load_json_data('boards.json')

    # Create a set of names from the device data
    device_names = {device['name'] for device in device_data}

    # Filter data based on the current time and the past 3 hours
    moisture_values = []
    for entry in data:
        if entry['time'] >= three_hours_ago:
            board_name = entry['payload']['board_name']
            if board_name in device_names:
                moisture_key = next((key for key in entry['payload'] if 'Moisture' in key), None)
                if moisture_key:
                    moisture_values.append(float(entry['payload'][moisture_key]))

    # Calculate the average moisture value
    avg_moisture = sum(moisture_values) / len(moisture_values) if moisture_values else 0
    return f"The average moisture in the past 3 hours is: {avg_moisture:.2f} RH% \n"

def compute_avg_water_consumption() -> str:
    data = mongo.get_dishwasher_data()
    water_values = [entry['water_usage'] for entry in data]
    avg_water = sum(water_values) / len(water_values) if water_values else 0
    return f"The average water consumption per cycle is: {avg_water:.2f} gallons\n"

def compute_device_energy_comparison() -> str:
    data = mongo.get_energy_data()
    energy_usage = {device['name']: device['energy'] for device in data}
    max_device = max(energy_usage, key=energy_usage.get)
    return f"The device that consumed the most electricity is: {max_device} with {energy_usage[max_device]:.2f} kWh\n"

