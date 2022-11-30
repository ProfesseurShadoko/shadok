
# Shadok

This is my personal python package, but it contains some usefull
tools like wrappers, dictionnaries (in French), ProgressBar, some
ProblemSolvers, etc.



## Installation

Install shadok where your Python Libraries are with :

```bash
  git clone https://github.com/ProfesseurShadoko/shadok.git
```

## Documentation

***Style***<br>
Print colored text : 
```python
from shadok.style import style
style = Style(style="underline",text="red",background="white")
print(style("Some text"))
```
***
***Wrappers***<br>
Implement Fibonacci :
```python
from shadok.wrappers import memoize_me

@memoize_me
def fib(n):
  if n in [0,1]:
    return 1
  else:
    return fib(n-1)+fib(n-2)
```

Time any function :
```python
from shadok.wrappers import time_me

@time_me
def test():
  return fib(30)
  
```

Intercept everything a function has printed :
```python
from shadok.wrappers import jam_me, JAMMER

@jam_me
def prints_stuff():
  print("stuff")
  
print_stuff() #doesn't print anything
JAMMER.print() #prints stuff
  
```

***

***Progress Bar***

Trough an Iteration :
```python
from shadok.progress_bar import ProgressIterator
from time import sleep

for i in ProgressIterator(range(0,100)):
  print(i)
  sleep(0.1)
```

Trough a wrapper:
```python
from shadok.progress_bar import ProgressBar, task_me

bar = ProgressBar(100)

@task_me(bar,1)
def wait():
  sleep(0.1)

for i in range(100):
  wait()  
```

***

***Dictionnary***
```python
from shadok.dictionnary import Wordle
from shadok.style import OK,FAIL

dico = Wordle()
word = "apple"

if dico[word]: #check weather the dictionnary contains a word
  OK()
else:
  FAIL()
```

***
***XLDB***

Implementation of a Database and Model via an Excel Sheet (requires openpyxl, script tries to install it automatically at start)

```python
from shadok.XLDB import Database,Model,Filter

class Admin(Model):
  def __init__(self,name:str):
    super().__init__()
    self.name = name
    
  @staticmethod
  def get_property_names() -> list:
    return ["name"]
 
Database.start()
Admin.create()

Admin("Professeur Shadoko").save()
print(Admin.get(1))
print(Admin.filter(Filter(lambda x:x.id<12,name="Professeur Shadoko"))[0])
```



    
