class Num:
    def __iter__(self):
        self.a=1
        return self
    def __next__(self):
        x=self.a
        self.a+=1

        return x
    
obj=Num()

it=iter(obj)

for i in range(10):
    print(next(it))