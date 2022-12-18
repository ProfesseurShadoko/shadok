import os

class Style:
    OCTAL = "\033["
    style = {
        "normal":"0",
        "reset":"0",
        "bold":"1",
        "b":"1",
        "italicized":"3",
        "i":"3",
        "underline":"4",
        "u":"4",
        "blink":"5",    
    }
    text = {
        "black":"30",
        "red":"31",
        "green":"32",
        "yellow":"33",
        "blue":"34",
        "purple":"35",
        "cyan":"36",
        "white":"37",
    }
    background = {
        "black":"40",
        "red":"41",
        "green":"42",
        "yellow":"43",
        "blue":"44",
        "purple":"45",
        "cyan":"46",
        "white":"47",
        "transparent":"49"
    }
    
    def __init__(self,style:str="normal",text:str="white",background:str="transparent"):
        self.style=style
        self.text=text
        self.background=background
    
    def __str__(self)->str:
        return Style.OCTAL + Style.style[self.style] + ";" + Style.text[self.text] + ";" + Style.background[self.background] + "m"
    
    def set(self)->None:
        print(self,end="")
    
    def __call__(self,text)->str:
        return self.__str__()+str(text)+Style().__str__()

class ANSI:
    """
    
- Position the Cursor:
  \033[<L>;<C>H
     Or
  \033[<L>;<C>f
  puts the cursor at line L and column C.
- Move the cursor up N lines:
  \033[<N>A
- Move the cursor down N lines:
  \033[<N>B
- Move the cursor forward N columns:
  \033[<N>C
- Move the cursor backward N columns:
  \033[<N>D

- Clear the screen, move to (0,0):
  \033[2J
- Erase to end of line:
  \033[K

- Save cursor position:
  \033[s
- Restore cursor position:
  \033[u
    """
    
    go_up = "\033[A"
    go_up_n_left = "\033[F"
    go_right = "\033[C"
    go_left = "\033[D"
    save="\033[s"
    restore="\033[u"
    erase_line="\033[K"

    


def OK(end="\n"):
    Style(text="green").set()
    print("OK",end=end)
    Style().set()

def FAIL(end="\n"):
    Style(text="red").set()
    print("FAIL",end=end)
    Style().set()

def WARNING(end="\n"):
    Style(text="yellow").set()
    print("WARNING",end=end)
    Style().set()

def CLEAR():
    """clears the console with os.system('cls')"""
    os.system('cls')

def ASSERT(condition:bool):
  """evaluates condition (true or false) and prints OK or FAIL

  """
  if condition:
    OK()
  else:
    FAIL()

if __name__=="__main__":
    OK()
    FAIL(end="")
    WARNING()