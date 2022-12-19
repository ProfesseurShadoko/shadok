from copy import deepcopy #recursive copy of an object, everything is copied
from functools import wraps

from shadok.memory import Loadable,autosave
from shadok.abstract import IncompleteClassDefinition



class Trainable(Loadable):
    """Inherits from Loadable ! run .deactivate_load() or simply never call .save() to avoid
    Function required : 
    - method apply_mutation(self)->None
    - @classmethod load(cls:type)->default instance of the class (for exemple for a neural network : a neural network filled with zeros)
    """
    
    memory_path:str="memory/champions"
        
    def __str__(self) -> str:
        return f"{type(self).__name__} object : generation={self.get_generation()}, score={self.get_score()}"
    
    def copy(self):
        """deepcopy (recursive copy of everthing) of the object. 
        """
        return deepcopy(self)
    
    def reward(self,points:float=1)->None:
        if not hasattr(self,"score"):
            self.score = 0
        self.score+=points
    
    def get_score_rwd(self)->float:
        if not hasattr(self,"score"):
            self.score=0
        return self.score
    
    def new_generation(self)->None:
        if not hasattr(self,"generation"):
            self.generation=1
        self.generation+=1
    
    def get_generation(self)->int:
        if not hasattr(self,"generation"):
            self.generation=1
        return self.generation
            
    def apply_mutations(self)->None:
        """random (or not) changes that have to be made when the object is "splitted", when the properties of the object are passed to it's child
        """
        raise IncompleteClassDefinition("apply_mutation()",type(self))
    
    @classmethod
    def load(cls:type):
        raise IncompleteClassDefinition("load()",cls)
    
    def split(self):
        """returns child of self (a copy with mutations applied, generation increased and score reset)
        """
        out = self.copy()
        out.apply_mutations()
        out.score=0
        out.new_generation()
        return out

class Population(Loadable):
    """Population is a set of Trainable objects that evolve from generation to generation.
    On initialisation, __init__ takes in input the class of the object you want to train (class must inherit from Trainable).
    You also give the size of the population.
    Population inherist from Loadable, so the training will restart from where it lasts stopped. Run Population.reset_memory() to restart.
    
    Usefull functions are the fllowing :
        - population.reward(citizen:int,points:float)
        - population.get(citizen:int) -> object of trained_class
        - population.filter(percent:float) => only keeps elements of the population that have been rewarded the most
    
    You must implement the following function :
        @autosave
        def train(self,generations,...):
            <repeat for each generation>
                <loop over the citizens>
                    <test citizen and reward if success>
                <filter population>
    Population will automatically be saved at the end of execution.
    
    If you want to train different population, change the memory_path.
    """
    
    memory_path="memory/populations"
    
    def __init__(self,cls:type,size:int=100):
        if size==0:
            raise(ZeroDivisionError())
        self.citizens:list=[]
        self.size:int=size
        self.cls = cls
        
        for _ in range(self.size):
            self.citizens.append(self.cls.load())
    
    def __str__(self)->str:
        return f"<{type(self).__name__} of {self.size} objects of type {self.cls.__name__}>"

    def avg_score(self)->float:
        return sum([citizen.get_score_rwd() for citizen in self.citizens])/len(self.citizens)
    
    def reward(self,citizen:int,points:float=1)->None:
        self.citizens[citizen].reward(points)
    
    def get(self,index:int)->Trainable:
        return self.citizens[index]
    
    def sort(self)->None:
        """sorts population by decreasing score (best score = best models = first)"""
        self.citizens.sort(key=lambda x:-x.get_score_rwd())
    
    def filter(self,percent:float=0.1):
        """if percent = 0.1, the ten best models remain and the rest of the population is filled with their children.
        """
        self.sort()
        to_keep = max(1,min(len(self.citizens),int(percent*len(self.citizens))))
        
        new_pop=[]
        for i in range(to_keep):
            self.get(i).score=0
            new_pop.append(self.get(i))
        
        for i in range(len(self.citizens)-to_keep):
            new_pop.append(self.get(i%to_keep).split())
        self.citizens = new_pop

    @autosave
    def train(self,generation:int=100):
        """train your population (using reward / filter). Use wrapper @autosave in order to save progression at the end or on keyboardinterupt"""
        raise IncompleteClassDefinition("train",type(self))


