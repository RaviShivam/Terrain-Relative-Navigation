
class Crater:
    def __init__(self, id, centerpoint, diameter):
        self.id = id
        self.centerpoint = centerpoint
        self.diameter = diameter

    def __str__(self):
        return "Crater: <centerpoint= {}, diameter= {}>".format(self.centerpoint, self.diameter)

    def __repr__(self):
        return self.__str__()


