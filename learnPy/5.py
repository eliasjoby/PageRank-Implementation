class Vehicle:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model

    def move(self):
        print("Move!!")
    
class Car(Vehicle):
    pass

class Boat(Vehicle):
    def move(self):
        print("Sail")

class Plane(Vehicle):
    def move(self):
        print("Fly")
    
car1=Car("a","aa")
boat1=Boat("b","bb")
plane1=Plane("c","cc")

for x in (car1,boat1,plane1):
    print(x.brand)
    print(x.model)
    x.move()
    
