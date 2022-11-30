import math


pi = math.pi

G = 6.674_30e-11
c = 299_792_458

#QUANTUM MECANICS
h = 6.626_070_15e-34
h_bar = h/2/pi

#ATOMS AND PARTICLES
e = 1.602_176_634e-19
m_e = 9.109_383_70e-31
m_p = 1.672_621_923e-27
m_n = 1.674_927_498e-27
a_zero = a_bohr = 5.291_772_109e-11

#ELECTROMAG
mu_zero = 1.256_637_062_12e-6
epsilon_zero = 1/mu_zero/c/c
k_b = 1.380_649e-23

#CHEMISTRY
N_a = N_avogadro = 6.022_140_76e23
F = N_a*e
R = N_a*k_b
u = dalton = 1/(N_a*1e3)

#RELATIVITE GENERALE
def gamma(v:float)->float:
    """returns relativist gamma constant"""
    return 1/math.sqrt(1-beta(v)**2)
    
def beta(v:float)->float:
    """returns v/c"""
    return v/c

