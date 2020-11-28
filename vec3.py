import math
import random

# operations on 3-tuples

def add(v1, v2):
    return tuple(v1[i] + v2[i] for i in range(3))

def subtract(v1, v2):
    return tuple(v1[i] - v2[i] for i in range(3))

def mult(v1, v2):
    return tuple(v1[i] * v2[i] for i in range(3))

def scale(v, a):
    return tuple(a * v[i] for i in range(3))

def dot(v1, v2):
    return sum(mult(v1, v2))

def cross(v1, v2):
    return (v1[1] * v2[2] - v1[2] * v2[1],
            -(v1[0] * v2[2] - v1[2] * v2[0]),
            v1[0] * v2[1] - v1[1] * v2[0])

def squared_length(v):
    return dot(v, v)

def length(v):
    return math.sqrt(squared_length(v))
    
def normalize(v):
    if length(v) == 0:
        return (0, 0, 0)
    return scale(v, 1/length(v))

def gamma_correct(v, gamma):
    return tuple(v[i]**(1.0/gamma) for i in range(3))

def rand_sphere():
    p = (random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1))
    return normalize(p)

def reflect(v, n):
    return subtract(v, scale(n,2*dot(v, n)))

def refract(v, n, idx_ratio):
    uv= normalize(v)
    dt = dot(uv, n)
    discriminant = 1.0 - idx_ratio**2 * (1 - dt**2)
    if discriminant > 0:
        refracted = scale(subtract(uv, scale(n, dt)), idx_ratio)
        refracted = subtract(refracted, scale(n, math.sqrt(discriminant)))
        return refracted
    return None
        
