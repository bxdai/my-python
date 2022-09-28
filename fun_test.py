# def funcB(fun):
#     print("funcb")
#     fun()
#     return "test"
 
# @funcB
# def funA():
#     print("funA")

# print(funA)

# def f():
#     print("f......")
#     return "sss"
# #s =f()
# print(f)

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper


@log
def now():
    print('2021-3-25')
    return "sss"


if __name__ == '__main__':
    # now()
    print(now)
