import random
import math
from tkinter import Tk, Canvas, PhotoImage, mainloop
import vec3
from ray import *
from materials import *

# canvas setup
width = 400
height = 200
window = Tk()
canvas = Canvas(window, width=width, height=height)
canvas.pack()
img = PhotoImage(width=width, height=height)
canvas.create_image((width//2, height//2), image=img, state="normal")

# camera setup
origin = (0.0, 0.0, 0.0)
lookat = (0.0, 0.0, -1.0)
up = (0.0, 1.0, 0.0)
fov = 90
aspect = width/height
camera = Camera(origin, lookat, up, fov, aspect)
n_samples = 10

# world setup
diffuse = Sphere((0.0, 0.0, -1.0), 0.5, Lambertian((0.8, 0.3, 0.3)))
metal = Sphere((1.0, 0.0, -1.0), 0.5, Metal((0.8, 0.6, 0.2)))
earth = Sphere((0.0, -100.5, -1.0), 100.0, Lambertian((0.8, 0.8, 0.0)))
world = HitableList([diffuse, metal, earth])
eps = 0.001 # threshold for hitting object with a ray

def from_rgb(rgb):
    #translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb

# world contains the hitable objects
def color(ray, world, depth):
    record = world.hit(ray, eps, float('inf'))
    if record:
        # camera receives color from a ray scattered randomly off surface
        if (depth < 10):
            scattered = record.material.scatter(ray, record)
            if scattered:
                return vec3.mult(color(scattered, world, depth+1), record.material.attenuation)
    unit = vec3.normalize(ray.direction)
    t = 0.5 * (unit[1] + 1.0)
    c1 = vec3.scale((1.0, 1.0, 1.0), 1.0 - t)
    c2 = vec3.scale((0.5, 0.7, 1.0), t)
    return vec3.add(c1, c2)

# note that height is reversed from C++
def draw():
    for j in range(height):
        for i in range(width):
            col = (0, 0, 0)
            for _ in range(n_samples):
                u = float(i + random.random()) / float(width)
                v = float(j + random.random()) / float(height)
                ray = camera.get_ray(u, v)
                col = vec3.add(col, color(ray, world, 1))
            col = vec3.scale(col, 1.0/n_samples)
            col = vec3.gamma_correct(col, 2.0)
            ir = int(255.99 * col[0])
            ig = int(255.99 * col[1])
            ib = int(255.99 * col[2])
            img.put(from_rgb((ir, ig, ib)), (i, height-j-1))
        print('drew row ' + str(j))
draw()
mainloop()
