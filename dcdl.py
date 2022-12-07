from shadok.dictionnary import Dictionnary,Dcdl,Scrabble
from shadok.wrappers import time_me
from shadok.style import Style


class LetterSolver:
    
    def __init__(self,letters:str,dictionnary:Dictionnary):
        self.letters = letters.replace(" ","").replace(",","").replace(";","").replace("\n","").replace(":","")
        self.letters = list(self.letters)
        self.letters.sort()
        self.remaining = [True]*len(self.letters)
        self.dicotree = dictionnary.dico
        self.current_word = ""
        self.best_words = []
    
    def run_aux(self):
        """finds solution by calling itself"""
        
        if self.dicotree.is_valid:
            if len(self.best_words)==0:
                self.best_words=[self.current_word]
            elif len(self.best_words[0])==len(self.current_word):
                self.best_words.append(self.current_word)
            elif len(self.best_words[0])<len(self.current_word):
                self.best_words = [self.current_word]
        
        for i in range(len(self.letters)):
            if self.remaining[i]:
                char = self.letters[i]
                if self.dicotree[char] != None:
                    tmp = self.dicotree
                    char = self.letters[i]
                    self.remaining[i]=False
                    self.current_word+=char
                    self.dicotree = self.dicotree[char]
                    
                    self.run_aux()
                    
                    self.dicotree = tmp
                    self.remaining[i]=True
                    self.current_word = self.current_word[:-1]

    def run(self):
        """solve and display solution"""
        self.show_solution()

    def show_solution(self):
        """solve and display solution"""
        self.run_aux()
        self.best_words = list(set(self.best_words))
        n = len(self.best_words[0])
        print(f"J'ai {n} lettres avec le(s) mot(s) :", *self.best_words, sep=" ")


class EndOfSearch(Exception):
    def __init__(self):
        super().__init__("Solution found !")
        
class ChiffreSolver:
    def __init__(self,numbers:list,target:int):
        self.numbers = numbers
        self.current = []
        self.target = target
        
        self.best = 0
        self.best_operations = []
        self.update(self.numbers)
    
    def run_aux(self,numbers:list):
        self.update(numbers)
        for i in range(len(numbers)):
            for j in range(i+1,len(numbers)):
                n1 = numbers[i]
                n2 = numbers[j]
                if n1<n2:
                    n1,n2=n2,n1
                
                for operation in ["+","-","*","//"]:
                    if operation != "//" or n1%n2==0:
                        new = eval(f"n1{operation}n2")
                        if new!=0:
                            new_list=[]
                            for k in range(len(numbers)):
                                if k!=i and k!=j:
                                    new_list.append(numbers[k])
                            new_list.append(new)
                            self.current.append(f"{n1}{operation}{n2}={new}")
                            self.run_aux(new_list)
                            self.current.pop()
    
    def update(self,numbers:list):
        """updates best result if necessary"""
        for number in numbers:
            if abs(self.target-self.best)>abs(self.target-number):
                self.best = number
                self.best_operations = self.current.copy()
                
                if self.best==self.target:
                    raise(EndOfSearch())
    
    def show_solution(self):
        """finds and show solution"""
        print()
        print(" ",*self.numbers, "-->",Style(text='green')(str(self.target)),sep="   ")
        print()
        if self.best==self.target:
            print(Style(text="green")("Le compte est bon !"))
        else:
            print(Style(text="yellow")(f"Il n'était pas possible de faire mieux que {self.best} !"))
        step:str
        for step in self.best_operations:
            print(step.replace("//","/"))
        print()
    
    def run(self):
        """solve and display solution"""
        try:
            self.run_aux(self.numbers)
        except EndOfSearch:
            pass
        self.show_solution()



                         
    
if __name__=="__main__":
    dico = Scrabble()
    solver = LetterSolver("abcdefghijklmnopqrstuvwxyz",dico)
    solver.run()
    #J'ai 14 lettres avec le(s) mot(s) : cryptogamiques stylographique xylographiques"""
    
    """
    numbers=[8,25,50,75,8,8]
    target = 827
    solver = ChiffreSolver(numbers,target)
    solver.run()"""
        
        