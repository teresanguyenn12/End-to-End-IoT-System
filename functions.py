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
        Question 1:
        Get average refrigerator moisture data within the past 3 hours
    '''
    data = mongo.get_data()
    current_time = datetime.now()

    # Compute the time for 3 hours ago
    three_hours_ago = current_time - timedelta(hours=3)

    # Load device data from the boards.json file
    board_data = load_json_data('boards.json')

    # Create a set of names from the device data
    board_names = {device['name'] for device in board_data}

    # Filter data based on the current time and the past 3 hours
    moisture_values = []
    for entry in data:
        if entry['time'] >= three_hours_ago:
            board_name = entry['payload']['board_name']
            if board_name in board_names:
                moisture_key = next((key for key in entry['payload'] if 'Moisture' in key), None)
                if moisture_key:
                    moisture_values.append(float(entry['payload'][moisture_key]))

    # Calculate the average moisture value
    avg_moisture = sum(moisture_values) / len(moisture_values) if moisture_values else 0
    print("Returning data...\n")
    return f"The average moisture in the past 3 hours is: {avg_moisture:.2f} RH% \n"
            

def compute_avg_water_consumption() -> str:
    '''
        Question 2:
        Get average water consumption per cycle in the smart dishwasher
    '''
    dishwasher_id = None

    # Load device data from the boards.json file
    boards = load_json_data('boards.json')
    devices = load_json_data('devices.json')

    # Get the device ID of the smart dishwasher
    for device in devices:
        if device['name'] == 'Smart Dishwasher':
            dishwasher_id = device['id']
            print(f"Found Smart Dishwasher ID: {dishwasher_id}")
            break

    # Find dishwasher board based on device ID
    for board in boards:
        if board['virtual_device'] == dishwasher_id:
            dishwasher_asset_id = board['asset_uid']
            print(f"Found Smart Dishwasher Board: {dishwasher_asset_id}")
            break

    # Get all dishwasher data based on asset ID from mongo db
    data = mongo.get_data(query={'payload.asset_uid': dishwasher_asset_id})

    water_values = []
    for entry in data:
        payload = entry['payload']
        if payload['Water Consumption']:
            water_values.append(float(payload['Water Consumption']))
    
    # Calculate the average water consumption per cycle
    avg_water_consumption = sum(water_values) / len(water_values) if water_values else 0

    print("Returning data...\n")
    return f"The average water consumption: {avg_water_consumption:.2f} gallons/ per cycle \n"

def compute_max_electricity_consumption() -> str:
    '''
        Question 3:
        Get the device that consumed the most electricity among two refrigerators and a dishwasher.
    '''
    # Load device data from the boards.json file
    board_data = load_json_data('boards.json')
    board_device_map = create_board_device_map(board_data)

    # Create a set of names from the device data
    # Get all data from the MongoDB
    data = mongo.get_data()

    boards = split_data_by_board(data)

    # Dictionary to store the total electricity consumption for each device
    electricity_consumption = []

    # Loop through 3 devices
    for board_name, board_data in boards.items():
        total_consumption = 0
        # Loop through n objects
        for entry in board_data:
            payload = entry['payload']
            # Loop through 8 - 10 keys, values
            for key, value in payload.items():
                if 'Current Sensor' in key:
                    total_consumption += float(value)
        electricity_consumption.append((board_name, total_consumption))
   
    # Find the device that consumed the most electricity
    max_board, max_consumption = max(electricity_consumption, key=lambda x: x[1])
    
    # Find device_name in boards.json and set it to the device_name
    max_device_name = board_device_map[max_board]
    print("Returning data...\n")
    return f"{max_device_name} consumed the most electricity with {max_consumption:.2f} kWh\n"


def create_board_device_map(data):
    """
    Creates a map with the board name as the key and the device name as the value.
    """
    board_device_map = {item["name"]: item["device_name"] for item in data}
    return board_device_map


def split_data_by_board(data) -> dict:
    '''
        Split data by device name
    '''
    device_data = {}
    for entry in data:
        board_name = entry['payload']['board_name']
        if board_name not in device_data:
            device_data[board_name] = []
        device_data[board_name].append(entry)
    
    return device_data
