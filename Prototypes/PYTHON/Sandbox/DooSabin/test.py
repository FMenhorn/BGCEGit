__author__ = 'anna'

class A:
    def __init__(self, property1, property2):
        self.p1 = property1
        self.p2 = property2

listOfObjects = []
for i in range(5):
    listOfObjects.append([A(i, i+1), A(i, i+1)])

print([listOfObjects[0][0], listOfObjects[1][1]] in listOfObjects)