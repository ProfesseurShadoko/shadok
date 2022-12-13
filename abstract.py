
from shadok.style import Style

def abstractmethod(func):
    func.__isabstract__=True
    return func

def abstractmethods(cls)->list:
    #all_methods = [object_name for object_name in dir(cls) if not object_name.startswith("__")]
    all_methods = dir(cls)
    out=[]
    
    for method in all_methods:
        object = getattr(cls,method)
        if getattr(object,"__isabstract__",False):
            out.append(method)
    return out

class AbstractMetaclass(type):
    
    def __call__(cls,*args,**kwargs):
        abstract = abstractmethods(cls)
        if abstract: #if not abstract==[]            
            raise TypeError("Following methods are required and haven't been implemeneted:\n - "+'\n - '.join(abstract))
        return super().__call__(*args,**kwargs)

#ABC = Abstract Base Class
class ABC(metaclass=AbstractMetaclass):

    pass


class ExempleAbstract(ABC):
    
    def __init__(self,*args,**kwargs):
        print(f"Success, {type(self).__name__}.__init__ successfully completed !")
    
    @abstractmethod
    def f(self):
        pass
    
    @abstractmethod
    def g(self):
        pass

class ExempleError(ExempleAbstract):
    
    def f(self):
        pass

class ExempleSuccess(ExempleAbstract):
    
    def f(self):
        pass
    
    def g(self):
        pass

if __name__=="__main__":
    try:
        ExempleError()
    except Exception as e:
        print(e)
    
    ExempleSuccess()


            