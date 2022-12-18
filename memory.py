import os
import shutil
import pickle
from functools import wraps
from abstract import IncompleteClassDefinition

class Memory:
    
    def __init__(self,dir_path:str="memory"):
        """initializes memory in the path you defined (carefull, on reset the path is deleted)

        Args:
            dir_path (str, optional): directories will be created recursivly using this path. Defaults to "memory".
        """
        self.dir_path = dir_path
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path,exist_ok=True)
    
    def reset(self)->None:
        """removes folder containing the memory"""
        shutil.rmtree(self.dir_path)
    
    def parse(self,file_name:str)->str:
        """Returns path_to_directory + "/" + file_name + ".shadok", ie the location of the variable

        Args:
            file_name (str): variable name

        Returns:
            str: location of variable .shadok file
        """
        return self.dir_path+"/"+file_name+".shadok"
    
    def save(self,var,var_name:str)->None:
        """Save var (as bytes) in the memory folder under the given name (extension .shadok)

        Args:
            var (Any): variable you want to save
            var_name (str): how you want to name it (usually same name as the variable)
        """
        
        with open(self.parse(var_name),"wb") as file: #write bytes
            pickle.dump(var, file)
        return
    
    def load(self,var_name:str):
        """Returns the variable you saved

        Args:
            var_name (str): name of the .shadok file

        Returns:
            Any
        """
        with open(self.parse(var_name),"rb") as file:
            tmp = pickle.load(file)
        return tmp

class LoadableMeta(type):
    """redefines __call__ function (when you create an instance of your class) by first checking if there is an instance present in the memory (following memory_path)"""
    
    def __call__(self, *args, **kwds):
        #remerber,self is a class !
        if self.memory_path==None:
            raise(IncompleteClassDefinition("memory_path",self))
        
        if not self.load_active:
            obj = super().__call__(*args,**kwds) #self is in super
            obj.__reloaded=False
            return obj
        try:            
            obj = Memory(self.memory_path).load(self.__name__)
            obj.__reloaded=True
            return obj
        except FileNotFoundError:
            obj = super().__call__(*args,**kwds)
            obj.__reloaded=False
            return obj

class Loadable(metaclass=LoadableMeta):
    """has metaclass. On call (when creating an instance of your class), first there will be checked if an instance of your class already exists in memory. If so, it will be reloaded.
    Following methods are at you disposal :
        - save(self)
        - is_reloaded(self)
        - deactivate_load(cls)
        - activate_load(cls)
        - reset_memory(cls)
    """
    memory_path = None
    load_active=True      
    
    def save(self)->None:
        """saves current model in memory. Instance saved in :
        f"{type(self).memory_path}/{type(self).__name__}.shadok
        Instance will autamatically be reloaded on next creation of the instance"
        """
        memory = Memory(f"{type(self).memory_path}")
        memory.save(self,f"{type(self).__name__}")
    
    def is_reloaded(self)->bool:
        """checks if current instance has been reloaded from existing instance in memory."""
        return self.__reloaded
    
    @classmethod
    def deactivate_load(cls:type)->None:
        """prevents class from loading from memory when called"""
        cls.load_active=False
    
    @classmethod
    def activate_load(cls:type)->None:
        """again, on each call, the class will first look into the memory to check if an instance is already existing"""
        cls.load_active=True
        
    @classmethod
    def reset_memory(cls:type)->None:
        """forget the last instance created. Next instance will be brand new."""
        Memory(cls.memory_path).reset()

if __name__=="__main__":
    
    class AI(Loadable):
        memory_path = "main"
        def __init__(self,id):
            self.id = id
        def __str__(self)->str:
            return f"Class : {type(self).__name__} | id={self.id}"
    
    from shadok.style import ASSERT
    
    ai=AI(0)
    print(ai)
    ASSERT(ai.id==0)
    ai.id=1
    ai.save()
    
    print("SECOND INIT (should reload)")
    ai = AI()
    print(ai)
    ASSERT(ai.id==1)
    
    print("DEACTIVATING LOAD")
    AI.deactivate_load()
    ai = AI(0)
    print(ai)
    ASSERT(ai.id==0)
    
    AI.reset_memory()