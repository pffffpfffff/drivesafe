class dummy:
    def __init__(self,a):
        self.a = a

l = [dummy(x) for x in range(10)]
print([x.a for x in l])
del l[3]
print([x.a for x in l])

