import json
import os
from pprint import pprint

from github import Github

from actions.constants import ACTION, EVENT_TRIGGERS, GITHUB_EVENT_NAME, GITHUB_EVENT_PATH


def cached(function):
    """Simple decorator function to cache return value of wrapped function."""
    cache = {}

    def wrapper(*args, **kwargs):

        # check whether cache should be taken into account
        use_cache = kwargs.pop('use_cache', True)

        # determine cache key
        key = str(args) + str([kwargs[x] for x in sorted(kwargs.keys())])

        if use_cache:
            if key not in cache:
                cache[key] = function(*args, **kwargs)
            result = cache[key]
        else:
            result = function(*args, **kwargs)

        return result

    # expose clear_cache to clear cache for this function
    wrapper.clear_cache = cache.clear

    return wrapper


def get_env_var(name):
    """
    Get value of environment variable with specified name.

    If the environment variable is not defined, an OSError exception is raised.
    """
    res = os.getenv(name)
    if res is None:
        raise OSError("$%s not defined" % name)

    return res


@cached
def get_event_data(verbose=False):
    """
    Return parsed JSON dict with event data (parsed from $GITHUB_EVENT_PATH).

    :param verbose: whether or not to also print event data using pprint
    """
    github_event_path = get_env_var(GITHUB_EVENT_PATH)

    with open(github_event_path) as fp:
        event_data  = json.load(fp)

    if verbose:
        pprint(event_data)

    return event_data


def verify_event_name(event_name):
    """Verify whether specified event name is a known event name."""
    if event_name not in EVENT_TRIGGERS:
        raise ValueError("Unknown event name encountered: %s" % event_name)


def get_event_name():
    """Determine name of event that triggered current workflow."""
    event_name = get_env_var(GITHUB_EVENT_NAME)
    verify_event_name(event_name)

    return event_name


def verify_activity_type(activity_type, event_name=None):
    """
    Verify whether specified activity type is valid for event with specified name.
    If 'event_name' is not specified, the name of the event that triggered the current workflow is used.
    """
    if event_name is None:
        event_name = get_event_name()

    if activity_type not in EVENT_TRIGGERS[event_name]:
        raise ValueError("Unknown type of '%s' event encountered: %s" % (event_name, activity_type))


def get_activity_type(event_name=None):
    """Determine activity type of event that triggered current workflow."""
    activity_type = get_event_data()[ACTION]
    verify_activity_type(activity_type)

    return activity_type


def get_event_trigger():
    """Determine the name + type of the event that triggered the current workflow."""
    event_name = get_event_name()
    activity_type = get_activity_type(event_name=event_name)

    return event_name + '.' + activity_type


def triggered_by(event_name, activity_type=None):
    """Check whether current workflow was triggered by event with specified name & activity type."""
    event_trigger = get_event_trigger()

    verify_event_name(event_name)

    if activity_type is None:
        res = event_trigger.startswith(event_name + '.')
    else:
        verify_activity_type(activity_type, event_name=event_name)
        res = event_trigger == event_name + '.' + activity_type

    return res
