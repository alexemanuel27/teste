class Decorator:

    def __init__(self, list_values: list[int]):
        self.list_values = list_values


    def decorator(self, func):

        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)
            output.extend(self.list_values)

            return output

        return wrapper


d = Decorator([1, 2, 3])

@d.decorator
def foo():
    return [4, 5, 6]

print(foo())