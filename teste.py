class User:

    def __init__(self, color):
        self._color = color

    @property
    def color(self):
    

u1 = User("azul")
print(u1.color)