class A:
    def __init__(self) -> None:
        pass
    def show(self):
        print("hello,world!")



def test():
    print("test....\n")

a = A()
a.show()
a.test = test
a.test()
a1 = A()
a1.num = 1

print("%d"%a1.num)
