import os
import sys
import time
from time import sleep
from functools import wraps

from .style import WARNING,OK,FAIL,CLEAR,Style
from .wrappers import time_me,memoize_me
from .physics import *

def help():
    print(open(os.path.dirname(__file__)+"/static/welcome.txt","r").read())

#  ━╸━━━━━━━━