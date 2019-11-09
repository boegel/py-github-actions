import os


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
