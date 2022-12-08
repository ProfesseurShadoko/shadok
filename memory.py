import os
import shutil
import pickle

class Memory:
    
    def __init__(self,dir_path:str="memory"):
        self.dir_path = dir_path
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
    
    def reset(self):
        shutil.rmtree(self.dir_path)
    
    def parse(self,file_name:str)->str:
        return self.dir_path+"/"+file_name+".shadok"
    
    def save(self,var,var_name:str):
        
        with open(self.parse(var_name),"wb") as file: #write bytes
            pickle.dump(var, file)
    
    def load(self,var_name:str):
        with open(self.parse(var_name),"rb") as file:
            tmp = pickle.load(file)
        return tmp

class Pet:
    
    def __init__(self,animal:str):
        self.animal = animal
    
    def __str__(self)->str:
        return f"Animal : {self.animal}"
    

class Dog(Pet):
    
    def __init__(self):
        super().__init__("Dog")
    
    def bark(self):
        print("wouf !")

class PetStore:
    
    def __init__(self):
        self.pets=[]
    
    def add(self,pet:Pet):
        self.pets.append(pet)
    
    def __str__(self)->str:
        return f"Pet-store : {' // '.join(['{'+str(pet)+'}' for pet in self.pets])}"
       

if __name__=="__main__":
    Memory().reset()
    
    memory = Memory()
    
    snoopy = Dog()
    memory.save(snoopy,"snoopy")
    
    snoopy = memory.load("snoopy")
    
    print(snoopy)
    snoopy.bark()
    
    ps = PetStore()
    ps.add(snoopy)
    
    memory.save(ps,"ps")
    ps = memory.load("ps")
    print(ps)