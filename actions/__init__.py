import json
import os

def get_event_data():
    """Return parsed JSON dict with event data (parsed from $GITHUB_EVENT_PATH)."""
    github_event_path = os.getenv('GITHUB_EVENT_PATH')
    if github_event_path is None:
        raise EnvironmentError("$GITHUB_EVENT_PATH not defined")

    with open(github_event_path) as fp:
        event_data  = json.load(fp)

    return event_data
