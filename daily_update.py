import argparse
from datetime import datetime
from data_access.daily_levels import DailyLevelsInterface
from data_access.mongo_access import MongoDbAccess
from data_access.threshold import ThresholdInterface
from data_access.users import UserInterface
from utils.utils import get_configuration

KEY_LIST = [
    'morning.before',
    'morning.onehour_after',
    'morning.twohour_after',
    'evening.before',
    'evening.onehour_after',
    'evening.twohour_after'
]

def valid_date_arguments(str):
    try:
        return datetime.strptime(str, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(str)
        raise argparse.ArgumentTypeError(msg)

def check_key_option(choice):
    options = KEY_LIST

    while True:
        try:
            choice = int(choice)
            if 1 <= choice <= len(options):
                print(f"You chose: {options[choice - 1]}")
                return options[choice - 1]
            else:
                print("Please choose one of the following options:")
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")

                choice = input(f"Invalid choice. Please enter a number between 1 and {len(options)}: ")
        except ValueError:
            choice = input(f"Invalid choice. Please enter a number between 1 and {len(options)}: ")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process program arguments.")
    parser.add_argument('-k', type=int, default=0, help='Key option number')
    parser.add_argument('-d', type=valid_date_arguments, default=datetime.now().date(), help='Date that you measured glycemic index')
    args = parser.parse_args()
    return {
        'input_key': check_key_option(args.k),
        'input_date': args.d
    }

def input_glucose_level():
    while True:
        try:
            num = float(input("Please enter blood glucose level: "))
            if num <= 0:
                print("That's not a positive number! Please try again.")
            else:
                return num
        except ValueError:
            print("That's not a number! Please try again.")

################################################################################
##################################### MAIN #####################################
################################################################################
if __name__ == "__main__":
    config = get_configuration()

    arg_list = parse_arguments()
    date_value = arg_list['input_date']
    key = arg_list['input_key']
    new_value = input_glucose_level()

    mongo_client = MongoDbAccess(config.mongodb.uri, config.mongodb.database)
    mongo_client.test_connection()
    user_interface = UserInterface(mongo_client, config.username)

    threshold_interface = ThresholdInterface(mongo_client, user_interface.user._id)
    threshold_interface.check_glucose_level(key, new_value)

    glucose_interface = DailyLevelsInterface(mongo_client, user_interface.user._id)
    glucose_interface.update_glucose_level(date_value, key, new_value)
