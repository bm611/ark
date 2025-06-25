import json
from datetime import datetime


def save_messages_to_log(messages):
    """
    Saves the given messages as a JSON file with a timestamp as the filename
    in the logs directory.

    Args:
        messages: The data to be saved, typically a list of message dictionaries.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"ark/logs/{timestamp}.json"
    log_path = log_filename
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to write log file: {e}")