import os
from shadok.progress_bar import ProgressIterator
from shadok.style import Style


class DicoTree:
    
    #file = os.path.dirname(__file__)+"/dico.txt"
    
    def __init__(self):
        """classic tree for word searching
        """
        self.is_valid=False
        self.children = [None for i in range(26)]
    
    def __getitem__(self,char:str):
        """
        Args:
            char (str): lowercase letter

        Returns:
            DicoTree or None: returns subtree corresponding to letter, returns None if no word corresponding to the letter
        """
        return self.children[ord(char.lower())-ord("a")]
    
    def __setitem__(self,char:str,object):
        self.children[ord(char.lower())-ord("a")]=object
    
    def __len__(self)->int:
        out=0
        if self.is_word():
            out+=1
        for char in self.next_chars():
            out+=len(self[char])
        return out

    def to_str(self,root:str="")->str:
        out=""
        if self.is_word():
            out=out+root+"\n"
        for char in self.next_chars():
            out=out+self[char].to_str(root+char)
        return out
    
    def is_word(self)->bool:
        return self.is_valid
    
    def next_chars(self)->list:
        """
        Returns:
            list[char]: list of characters that correspond to valid subtrees
        """
        return [chr(ord("a")+i) for i in range(26) if self.children[i]!=None]
        
    def contains(self,word:str)->bool:
        if len(word)==0:
            return self.is_valid
        
        next_char,new_search = word[0],word[1:]
        child = self[next_char]
        
        if (child==None):
            return False
        else:
            return child.contains(new_search)
    
    def append(self,char:str)->None:
        """Appends empty DicoTree to children

        """
        if (self[char]==None):
            self[char]=DicoTree()
    
    def append_word(self,word:str)->None:
        """Append word to root

        Args:
            word (str): lowercase word !
        """
        if (len(word)==0):
            self.is_valid=True
        else:
            char,rest = word[0],word[1:]
            self.append(char)
            self[char].append_word(rest)
    
    @staticmethod
    def create(filename:str):
        """creates DicoTree from words in filename
        """
        words=open(filename,"r").readlines()
        dico = DicoTree()
            
        for word in ProgressIterator(words,message="Creating dictionnary..."):
            word = word.replace("\n","")
            dico.append_word(word)
            
        return dico


class Dictionnary:
    
    def __init__(self,filename:str="DEFAULT"):
        """creates a dictionnary from your own list of words

        Args:
            filename (str): .txt file that contains one word per line (without '.txt' wich is added automatically)
        """
        if (filename=="DEFAULT"):
            filename = os.path.dirname(__file__)+"/static/dcdl.txt"
        else:
            filename = os.path.dirname(__file__)+f"/static/{filename}.txt"
        self.dico = DicoTree.create(filename)
        self.size = len(self.dico)
    
    def contains(self,word:str)->bool:
        """searches word in the dictionnary

        Args:
            word (str): algorithm not case sensitive

        Returns:
            bool: if the dictionnary (DCDL) contains a word
        """
        return self.dico.contains(word)
    
    def __str__(self)->str:
        """
        Returns:
            str: content of input file in alphabetic order
        """
        return self.dico.to_str()

    def __len__(self)->int:
        return self.size
    
    def __getitem__(self,word:str)->bool:
        """check if dicitonnary contains word

        Args:
            word (str)

        Returns:
            bool
        """
        return self.contains(word)

    def run(self):
        word = input("Mot à vérifier : ")
        if word in ["q","quit","quit()"]:
            return
        else:
            try:
                exists = self[word]
            except:
                exists = False
            if exists:
                print(f"Le mot '{Style(text='green')(word)}' est valide !")
            else:
                print(f"Le mot '{Style(text='red')(word)}' est invalide !")
                
            self.run()

class Dcdl(Dictionnary):
    
    def __init__(self):
        super().__init__()

class Scrabble(Dictionnary):
    
    def __init__(self):
        super().__init__("ods5")

class Wordle(Dictionnary):
    
    def __init__(self):
        super().__init__("wordle")

if __name__=="__main__":
    Dcdl()
    Scrabble()
    Wordle()





    
    
        
        