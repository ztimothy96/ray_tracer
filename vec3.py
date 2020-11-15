import math

# operations on 3-tuples
def add(v1, v2):
    return tuple(v1[i] + v2[i] for i in range(3))

def scale(v, a):
    return tuple(a * v[i] for i in range(3))

def dot(v1, v2):
    return sum(tuple(v1[i] * v2[i] for i in range(3)))

def cross(v1, v2):
    return (v1[1] * v2[2] - v1[2] * v2[1],
            -(v1[0] * v2[2] - v1[2] * v2[0]),
            v1[0] * v2[1] - v1[1] * v2[0])

def squared_length(v):
    return dot(v, v)

def length(v):
    return math.sqrt(squared_length(v))
    
def normalize(v):
    return scale(v, 1/length(v))
