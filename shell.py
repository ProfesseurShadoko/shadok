
from shadok.style import OK,FAIL,Style
from shadok.dictionnary import Scrabble,Dcdl
from shadok.dcdl import LetterSolver, ChiffreSolver

class ExitShell(Exception):
    def __init__(self):
        super().__init__("Exiting shell...")

def clean(input:str,*args:str):
    out = input
    for arg in args:
        out = out.replace(arg,"")
    return out


class Shell:
    
    def __init__(self,name:str=None,is_root:bool=False):
        print()
        print(self.help())
        self.name = name
        self.is_root=is_root
    
    def shell_env(self)->str:
        if self.name==None or self.name=="":
            return "--> "
        else:
            return f"[{self.name}] --> "
    
    def execute(self,command:str)->None:
        pass
    
    def get_commands(self)->dict:
        return {
            "-q":"Exit Shell"
        }
    def help(self)->str:
        out=">>> Commands :\n"
        for command,text in self.get_commands().items():
            out+=f" - '{command}' => {text}\n"
        return out
    
    def standard_verif(self,command)->None:
        if command=="-q":
            raise(ExitShell())
        
        if "python.exe" in command:
            raise(ExitShell())
    
    def loop(self)->None:
        command = input(self.shell_env())
        self.standard_verif(command)
        self.execute(command)
        self.loop()
    
    def run(self)->None:
        try:
            self.help()
            self.loop()
        except ExitShell:
            pass
        if not self.is_root:
            raise(ExitShell())

class BaseShell(Shell):
    
    def __init__(self):
        super().__init__(name="shadok",is_root=True)
    
    def execute(self, command: str) -> None:
        if command == "-l":
            return LetterShell().run()
        if command == "-s":
            return ScrabbleShell().run()
        if command == "-c":
            return ChiffreShell().run()
        return print(Style(text="red")("I am sorry, I don't know what you mean..."))
    
    def get_commands(self) -> dict:
        dict = super().get_commands()
        dict["-l"] = "Open 'Le mot le plus long' Solver"
        dict["-s"] = "Open Scrabble Validator"
        dict["-c"] = "Open 'Le compte est bon' Solver"
        return dict
        
class ScrabbleShell(Shell):
    
    def __init__(self):
        super().__init__("scrabble")
        self.dico = Scrabble()
    
    def execute(self, command: str) -> None:
        if command == "-l":
            return LetterShell().run()
        if command == "-c":
            return ChiffreShell().run()
        if "-s" in command:
            solver = LetterSolver(clean(command.lower()," ",":","[","]",",","-"),self.dico)
            solver.show_solution()
        else:
            command = command.lower().replace(" ","").replace("-","")
            if not command.isalpha():
                print(Style(text="red")("I am sorry, I don't know what you mean..."))
            else:
                if self.dico[command]:
                    print(Style(text="green")(command)+" is valid")
                else:
                    print(Style(text="red")(command)+" is invalid")
        
    def get_commands(self) -> dict:
        dict = super().get_commands()
        dict["-l"] = "Open 'Le mot le plus long' Solver"
        dict["-c"] = "Open 'Le compte est bon' Solver"
        dict["-s"] = "Solve best word for the following letters"
        dict["some word"] = "Check if a word exists"
        return dict

class LetterShell(Shell):
    
    def __init__(self):
        super().__init__("lettres")
        self.dico = Dcdl()
        self.scrabble = Scrabble()
    
    def execute(self, command: str) -> None:
        if command == "-s":
            return ScrabbleShell().run()
        if command == "-c":
            return ChiffreShell().run()
        
        if "-v" in command:
            command = clean(command.lower()," ","-v","-")
            if not command.isalpha():
                return print(Style(text="red")("I am sorry, I don't know what you mean..."))
            else:
                if self.dico[command]:
                    print(Style(text="green")(command)+" is valid")
                else:
                    print(Style(text="red")(command)+" is invalid")
                return
        command = clean(command.lower()," ",":","[","]",",","-")
        if not command.isalpha():
            return print(Style(text="red")("I am sorry, I don't know what you mean..."))
        solver = LetterSolver(command,self.dico)
        solver.show_solution()
        
    def get_commands(self) -> dict:
        dict = super().get_commands()
        dict["-c"] = "Open 'Le compte est bon' Solver"
        dict["-s"] = "Open 'Scrabble'"
        dict["-v"] = "Check if the following word is in the scrabble dictionnary"
        dict["some letters"] = "Solve best word for the letters"
        return dict

class ChiffreShell(Shell):
    
    def __init__(self):
        super().__init__("chiffres")
    
    def execute(self, command: str) -> None:
        if command == "-s":
            return ScrabbleShell().run()
        if command == "-l":
            return LetterShell().run()
        if command == "-c" or command =="":
            target = int(input("Target : "))
            numbers = input("Numbers (separated by one space) : ")
            numbers = [int(number) for number in numbers.split(" ")]
            solver = ChiffreSolver(numbers,target)
            return solver.run()
        return print(Style(text="red")("I am sorry, I don't know what you mean..."))
        
    def get_commands(self) -> dict:
        dict = super().get_commands()
        dict["-l"] = "Open 'Le mot le plus long' Solver"
        dict["-s"] = "Open 'Scrabble'"
        dict["-c"] = "Enter problem to resolve"
        return dict
    
BaseShell().run()