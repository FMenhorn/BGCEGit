__author__ = 'benjamin'

class A:
    id_counter = 0

    def __init__(self):
        self.id = A.id_counter
        A.id_counter += 1
        print "A with id = "+str(self.id)+ " created."

    @classmethod
    def with_id(self,id):
        self.id = id
        print "A with id = "+str(self.id)+ " created."


A()
A()
A()
