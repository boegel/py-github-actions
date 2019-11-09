import json
import os
from pprint import pprint

from github import Github


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
    github_event_path = get_env_var('GITHUB_EVENT_PATH')

    with open(github_event_path) as fp:
        event_data  = json.load(fp)

    if verbose:
        pprint(event_data)

    return event_data


def get_event_trigger():
    """Determine the name + type of the event that triggered the current workflow."""
    event_name = get_env_var('GITHUB_EVENT_NAME')

    event_data = get_event_data()
    event_type = event_data['action']

    return event_name + '.' + event_type
