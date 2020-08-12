import inspect
import timeit
import tracemalloc


def rate_performance(object, *args):
    print("Start rating...")

    rate = {}

    functions = get_functions(object)
    for func in functions:
        rate.update({func[0]: check_time(func[1], *args)})

    rate = {k: v for k, v in sorted(rate.items(), key=lambda item: item[1])}
    print(rate)


def get_functions(object):
    return [method for method in inspect.getmembers(object, inspect.ismethod)]


def check_time(function, *args):
    return timeit.timeit(lambda: function(*args))


def check_memory(function, *args):
    tracemalloc.start()

    function(*args)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    tracemalloc.stop()
