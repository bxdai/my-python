# =============单线程下执行===============
import threading
class Singleton(object):

    _instance_lock = threading.Lock()
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    # 类加括号就回去执行__new__方法，__new__方法会创建一个类实例：Singleton()
                    Singleton._instance = object.__new__(cls)  # 继承object类的__new__方法，类去调用方法，说明是函数，要手动传cls
        return Singleton._instance  #obj1
        # 类加括号就会先去执行__new__方法，在执行__init__方法
# obj1 = Singleton()
# obj2 = Singleton()
# print(obj1,obj2)

# ===========多线程执行单利============
def task(arg):
    obj = Singleton()
    print(obj)

for i in range(10):
    t = threading.Thread(target=task,args=[i,])
    t.start()

# 使用先说明，以后用单例模式，obj = Singleton()
# 示例
# obj1 = Singleton()
# obj2 = Singleton()
# print(obj1,obj2)

class A:
    pass



print(type(A))

#%%
import threading
class TaskManager:
    _instance_lock = threading.Lock()
    def __init__(self) -> None:
        pass
    def __new__(cls, *args, **kwargs) -> type:
        with TaskManager._instance_lock:
                if not hasattr(TaskManager, "_instance"):
                    TaskManager._instance = object.__new__(cls)
        return TaskManager._instance  #obj1
    # def __call__(self, *args: Any, **kwds: Any) -> Any:
    #     pass
    def root_dir(self) -> str:
        return self.rootdir

    def set_root_dir(self, dir: str):
        self.rootdir = dir
obj1 = TaskManager()
print(obj1)

obj2 = TaskManager()
print(obj2)
# %%
