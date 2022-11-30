
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
from shadok.wrappes import memoize_me

@memoize_me
def fib(n):
  if n in [0,1]:
    return 1
  else:
    return fib(n-1)+fib(n-2)
```

Time any function :
```python
from shadok.wrappes import time_me

@time_me
def test():
  return fib(30)
  
```

Intercept everything a function has printed :
```python
from shadok.wrappes import jam_me, JAMMER

@jam_me
def prints_stuff():
  print("stuff")
  
print_stuff() #doesn't print anything
JAMMER.print() #prints stuff
  
```

***



    
