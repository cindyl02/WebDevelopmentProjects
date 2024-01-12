import time


def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
        function()

    return wrapper_function


@delay_decorator
def say_hi():
    print("hi")


def say_greeting(greeting):
    print(greeting)


say_hi()
say_greeting("how are you?")
