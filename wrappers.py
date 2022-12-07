from time import perf_counter
from functools import wraps #non nécessaire mais permet de faire hériter la doc et le nom de la fonction
from shadok.style import OK,FAIL


def time_me(func):

    @wraps(func) #make sure thet doc from function and name are not erased by wrapper
    def wrapper(*args,**kwargs):

        #print function status
        str_args = ""
        for arg in args:
            arg_str = str(arg)
            if len(arg_str)>20:
                if hasattr(arg,"__len__"):
                    arg_str = f"<{type(arg)} object of size {len(arg)}>"
                else:
                    arg_str = f"<{type(arg)} object>"
            str_args+=f"{arg_str},"
        for kw in kwargs:
            str_args+=f"{kw}={kwargs[kw]},"
        print(f"You called : {func.__name__}({str_args[:-1]})")

        #execute function
        start_time = perf_counter()
        out=func(*args,**kwargs)
        total = perf_counter()-start_time
        try:
            print(f"Function returned {out} after :",total,"seconds\n")
        except:
            print("Function ended after :",total,"seconds\n")
        return out
    
    return wrapper

def memoize_me(func):
    #usefull for recursive functions
    cache={}
    @wraps(func)
    def wrapper(*args,**kwargs):
        key = str(args)+str(kwargs)
        if not key in cache.keys():
            cache[key]=func(*args,**kwargs)
        return cache[key]
    return wrapper

def try_me(func):
    
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            out=func(*args,**kwargs)
            OK()
            return out
        except Exception as e:
            FAIL(end=" --> ")
            print(e)
    return wrapper



        
    


if __name__=="__main__":
    
    ###
        
    print("\n@time_me")
    @time_me
    def squares():
        n=0
        for i in range(1000000):
            n+=i**2
        return n
    squares()
    
    ###
    
    print("\n@memoize_me")
    @try_me
    @time_me
    def run_fibo(N=100):
        @memoize_me
        def fibo(n):
            if n in [0,1]:
                return 1
            return fibo(n-1)+fibo(n-2)
        fibo(N)
    run_fibo(100)
    
    
    ###
    
    print("\n@try_me")
    @try_me
    def this_fails():
        raise Exception("This fails for a random reason")
    @try_me
    def this_succedes():
        pass
    this_fails()
    this_succedes()
    
    
    
    
    
     
            
        

#ça marche aussi avec des classes et un __init__