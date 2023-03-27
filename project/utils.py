def time_cache(seconds_to_cache):
    def give_time_parameter(fn):
        def new_fn(time_param, *args, **kwargs):
            return fn(*args, **kwargs)

        return new_fn

    def time_cache_real(fn):
        import time
        from functools import lru_cache

        cached_with_time_param = lru_cache(5)(give_time_parameter(fn))

        def provide_time(*args, **kwargs):
            return cached_with_time_param(
                time.time() // seconds_to_cache, *args, **kwargs
            )

        return provide_time

    return time_cache_real
