import json
import os
from pprint import pprint


def get_env_var(name):
    """
    Get value of environment variable with specified name.

    If the environment variable is not defined, an OSError exception is raised.
    """
    res = os.getenv(name)
    if res is None:
        raise OSError("$%s not defined" % name)

    return res


def get_event_data(verbose=False):
    """
    Return parsed JSON dict with event data (parsed from $GITHUB_EVENT_PATH).

    :param verbose: whether or not to also print event data using pprint
    """
    github_event_path = get_env_var('GITHUB_EVENT_PATH')

    with open(github_event_path) as fp:
        event_data  = json.load(fp)

    if verbose:
        pprint(event_data)

    return event_data


def get_event_name():
    """Determine the name of the event that triggered the current workflow."""
    return get_env_var('GITHUB_EVENT_NAME')
