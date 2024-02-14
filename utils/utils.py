import json
import os
import types

CONFIGURATION_ENVIRONMENTAL_VARIABLE_NAME = 'glucose_env'

def get_configuration():
    configuration_name = os.getenv(CONFIGURATION_ENVIRONMENTAL_VARIABLE_NAME, 'develop')

    # Read the JSON file
    file_path = f'configuration/{configuration_name}.json'
    with open(file_path, 'r') as f:
        data = json.load(f)

    if (
        (data['mongodb'] is None) or
        (data['mongodb']['uri'] is None) or
        (data['mongodb']['database'] is None) or
        (data['username'] is None) or
        (data['backup_file_name'] is None)
    ):
        raise ReferenceError("Error configuration file") 

    result = types.SimpleNamespace()
    result.mongodb = types.SimpleNamespace()
    result.mongodb.uri = data['mongodb']['uri']
    result.mongodb.database = data['mongodb']['database']
    result.username = data['username']
    result.backup_file_name = data['backup_file_name']
    return result

def check_folder(folder_relative_path):
    if not os.path.exists(folder_relative_path):
        os.makedirs(folder_relative_path)