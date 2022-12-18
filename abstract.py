
class IncompleteClassDefinition(Exception):
     def __init__(self, missing:str, cls:type) -> None:
         super().__init__(f"<{cls.__name__}> requires that the following property is defined : {cls.__name__}.{missing}")

def abstractmethod(func):
    """wrapper that allows to require that a subclass of ABC to implement a method.
    """
    func.__isabstract__=True
    return func

def abstractmethods(cls)->list:
    """Are you sure you want to use this function ? Don't you want to use "@abstractmethod" ? """
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
    """ABC stands for Abstract Base Class.
    When you inherit from this class, you inherit some methods marked by a wrapper as "abstract". If you don't implement those function, they will still be marked as abstract and raise and Exception when trying to build an instance of the class.
    This class is implemented with a metaclass that reimplments __call__. If you use an other metaclass, there will be a metaclass conflict.
    """
    pass




if __name__=="__main__":
    
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
        
    try:
        ExempleError()
    except Exception as e:
        print(e)
    
    ExempleSuccess()
    
    


            