from shadok.style import Style, ANSI
from shadok.jammer import Jammer
import time
from functools import wraps


class ProgressBar:
    """Allows to print a progressbar in the console
    
    Important functions :
        complete_task --> adds to progress
        __str__ --> shows progressbar
    """
    
    def __init__(self,goal:int=100,message:str="Processing...",bar_width:int=40):
        """Initialises progress bar

        Args:
            goal (int, optional): How many 'points' shall be scored to do the job ? Defaults to 100.
            message (str, optional): Defaults to "Processing...".
            bar_width (int, optional): Defaults to 40.

        """
        
        if (goal==0):
            raise ZeroDivisionError()
        self.message = message
        self.goal = goal
        self.progress=0
        self.start_time=time.perf_counter()
        self.initialised=False
        self.bar_width = bar_width
        self.jammer=Jammer()
        self.jammer.activate()
    
    def complete_task(self,task_value:int=1):
        """Adds points to the progress bar

        Args:
            task_value (int, optional): how closer shall we get to the goal ? Defaults to 1.
        """
        self.progress+=task_value
    
    def set_progress(self,progress:int=0):
        self.progress=progress
        
    def get_current(self)->int:
        return min(self.progress,self.goal)
    
    def get_progress(self)->float:
        """
        Returns:
            float: percentage of goal
        """
        return self.get_current()/self.goal
    
    def __str__(self)->str:
        blank = " "
        
        valid_range = int(self.get_progress()*self.bar_width)
        invalid_range = self.bar_width - valid_range
        
        
        #valid_bar=Style(text="green",background="green")(blank*valid_range)
        #invalid_bar=Style(text="red",background="red")(blank*invalid_range)
        
        blank="━"
        valid_bar=Style(text="green")(blank*valid_range+"╸")
        invalid_bar=Style(text="red")(blank*invalid_range)
        
        if self.get_progress()==1:
            style = Style(text="green")
        else:
            style=Style(text="yellow")
        
        percent = " " + style(f"{round(self.get_progress()*100,1)}%")
        time = " - "+Style(text="yellow")(str(round(self.get_time(),3))+"s")
        
        return self.message + " " + valid_bar + invalid_bar + percent + time
    
    def __repr__(self):
        return f"<ProgressBar : {self.get_current()}/{self.goal}> , {self.get_time()}s>"
    
    def get_time(self)->float:
        """Time since progress bar started
        """
        return time.perf_counter() - self.start_time
    
    def update(self,delay=0.01):
        """Displays the progress bar by deactivating, printing and reactivating the jammer

        Args:
            delay (float, optional): if the iteration is too fast, we don't want to be printing the progress bar too fast, so we display only if delay has past since last display. Defaults to 0.01.
        """
        if (self.progress>self.goal):
            return
        if not self.initialised:
            self.initialised=True
            self.previous_time=self.get_time()-delay-1
            self.jammer.deactivate()
            print(str(self),end="\r")
            self.jammer.activate()
        
        if self.progress==self.goal:
            self.jammer.deactivate()
            print(ANSI.erase_line+str(self))
            print(self.jammer,end="")
            return
            
        if self.get_time()-self.previous_time < delay:
            return
        
        self.previous_time=self.get_time()
        self.jammer.deactivate()
        print(ANSI.erase_line+str(self),end="\r")
        self.jammer.activate()



class Task:
    """Structure to add points to a progress bar
    """
    def __init__(self,bar:ProgressBar,value:int=1):
        self.value=value
        self.progress_bar=bar
    
    def complete(self):
        self.progress_bar.complete_task(task_value=self.value)
        self.progress_bar.update()

def task_me(bar:ProgressBar,value:int):
    """Set the corresponding task to a function (ProgressBar is incremented and displayed each time the function is executed)

    Args:
        bar (ProgressBar): _description_
        value (int): _description_

    Returns:
        decorator
    """
    task = Task(bar,value)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            task.complete()
            return func(*args,**kwargs)
        return wrapper
    return decorator

class ProgressIterator:
    
    def __init__(self,object,message:str="Processing..."):
        target=len(object)
        self.iter = iter(object)
        self.progress = ProgressBar(target,message)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        out = next(self.iter)
        Task(self.progress).complete()
        return out


if __name__=="__main__":
    n=0
    for i in ProgressIterator(range(0,100)):
        time.sleep(0.1)
        print(str(i)+",",end="")

    
    def sum(n):
        progress_bar = ProgressBar(n)
        
        @task_me(progress_bar,1)
        def square(i):
            if(i==10):
                print("10 has been reached")
            time.sleep(0.1)
            return i**2
        
        out=0
        for k in range(n):
            out+=square(k)
        return out
    
    print(sum(100))
    
    
    
    
    
    
    

    
