from data_access.mongo_access import MongoDbAccess
from data_access.daily_levels import DailyLevelsInterface
from data_access.users import UserInterface
import pandas as pd
from utils.utils import *

################################################################################
##################################### MAIN #####################################
################################################################################
if __name__ == "__main__":
    config = get_configuration()

    mongo_client = MongoDbAccess(config.mongodb.uri, config.mongodb.database)
    mongo_client.test_connection()
    user_interface = UserInterface(mongo_client, config.username)
    glucose_interface = DailyLevelsInterface(mongo_client, user_interface.user._id)
    docs = glucose_interface.getAllGlucoseData()

    check_folder('backup_data')
    output_path = f'backup_data/{config.backup_file_name}'
    data_frame = pd.DataFrame(list(docs))
    expanded_data = pd.json_normalize(data_frame['morning'])
    expanded_data.columns = ['morning_' + str(col) for col in expanded_data.columns]
    data_frame = data_frame.drop('morning', axis=1).join(expanded_data)
    expanded_data = pd.json_normalize(data_frame['evening'])
    expanded_data.columns = ['evening_' + str(col) for col in expanded_data.columns]
    data_frame = data_frame.drop('evening', axis=1).join(expanded_data)
    data_frame = data_frame.drop('_id', axis=1)
    data_frame = data_frame.drop('user_id', axis=1)
    data_frame.to_csv(output_path, index=False)