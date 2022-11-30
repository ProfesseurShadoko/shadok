import os 
import sys
from functools import wraps
from shadok.style import ANSI

#à transformer en environnement ?

class Jammer:
    """remplace sys.stdout\n
    self.print() et __str__ sont à disposition pour réccupérer le contenu intercepté
    """

    def __init__(self):
        self.stuff=""
        self.memory=""
        self.sys_stdout = sys.stdout
        self.flush= lambda :0
        self.is_active=False
        self.record_only=False
    
    def write(self,stuff)->None:
        self.stuff+=str(stuff)
        self.memory+=str(stuff)
        if (self.record_only):
            self.print()
    
    def print(self)->None:
        """print le contenu intercepté par le jammer depuis le dernier print
        """
        tmp = self.stuff
        self.stuff=""
        if (self.is_active):
            self.deactivate()
            print(tmp,end="")
            self.activate()
        else:
            print(tmp,end="")
        
    
    def __str__(self)->str:
        """
        Returns:
            str: contenu intercepté
        """
        return self.memory
    
    def __repr__(self)->str:
        return str(self).__repr__()
    
    def activate(self):
        """Starts the jammer, everything printed will be hidden and remembered by the jammer
        """
        self.is_active=True
        sys.stdout = self    
    
    def deactivate(self):
        """Frees the print function
        """
        self.is_active=False
        sys.stdout = self.sys_stdout
    
    def get_memory_size(self)->int:
        """Counts number of lines in jammer memory

        Returns:
            int: number of "\ n" caracters in memory
        """
        return self.memory.count("\n")
    
    def reset(self):
        """Erase memory
        """
        self.memory=""
        self.stuff=""
    
    def erase(self,add_one=False):
        """Erase everything the jammer memory has printed

        Args:
            add_one (bool, optional): Should we erase one more line, if 'print' has been used on jammer memory ("\ n" automatically added). Defaults to False.
        """
        lines = self.get_memory_size()
        if add_one:
            lines+=1
        if self.is_active:
            self.deactivate()
            for i in range(lines):
                print(ANSI.go_up_n_left+"\n"+ANSI.go_up_n_left,end="")#je monte, newline pour effacer, puis je remonte
            self.activate()
        else:
            for i in range(lines):
                print(ANSI.go_up_n_left+ANSI.erase_line,end="")#je monte, newline pour effacer, puis je remonte
    

JAMMER = Jammer()

def jam_me(jammer=JAMMER):
    """intercepte tout fonction "print()" que la fonction aurait pu appeler

    Args:
        jammer (Jammer, optional): intercepte ce que la fonction print. Si besoin de le réccupérer, créer un objet Jammer et le passer en argument. Defaults to Jammer().

    Returns:
        function: decorateur
    """
    
    #la fonction renvoie un décorateur !! (si elle n'est pas elle-même un décorateur, cf return)
    
    
    def tmp_decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            jammer.activate()
            try:
                return func(*args, **kwargs)
            finally:
                jammer.deactivate() 
        return wrapper
    
    if type(jammer)!=Jammer:
        #j'ai appelé @jam_me sans mettre de paranthèse, c'est la fonction qui a été balancée dedans
        func=jammer
        jammer=JAMMER
        @wraps(func)
        def wrapper(*args,**kwargs):
            jammer.activate()
            try:
                return func(*args, **kwargs)
            finally:
                jammer.deactivate() 
        return wrapper
    
    return tmp_decorator

if __name__=="__main__":
    jam = Jammer()
    print("Ceci n'est pas intecepté")
    print("Activating jam...")
    jam.activate()
    print("Ceci est intercepté")
    jam.deactivate()
    print("jam has been deactivated !")
    jam.print()
    
    print("@jam_me")
    @jam_me
    def print_stuff(stuff):
        print(stuff)
    
    print_stuff("Ceci est intercepté")
    JAMMER.print()
    
    print("\n\nLet's do some more tests !\n######\n")
    JAMMER.reset()
    print("Jammer starts here")
    JAMMER.activate()
    print("This is one line\nThis is a second line")
    JAMMER.deactivate()
    print("Jammer offline")
    JAMMER.print()
    JAMMER.erase()
    print(JAMMER.get_memory_size())
    
    print(JAMMER)
    import time
    time.sleep(1)
    JAMMER.erase(add_one=True)
    
    