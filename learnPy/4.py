class Num:
    def __iter__(self):
        self.a=1
        return self
    def __next__(self):

        if self.a<=20:
            x=self.a
            self.a+=1
            return x
        else:
            raise StopIteration
        
bruh=Num()
it=iter(bruh)

for i in it:
    print(i)

    