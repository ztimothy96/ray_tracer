# random circles in Tkinter
# a left mouse double click will idle action for 5 seconds and
# save the canvas drawing to an image file
# the Tkinter canvas can only be saved in postscript format 
# run PIL imagedraw simultaneously which
# draws in memory, but can be saved in many formats
# modified vegaseat's code from (circles):
# http://www.daniweb.com/software-development/python/code/216626
# and (simultaneous PIL imagedraw):
# http://www.daniweb.com/software-development/python/code/216929

import time
import random
import math
import tkinter as tk
import vec3
from ray import *
from materials import *
from PIL import Image, ImageDraw

# create the window form
root = tk.Tk()
# window title text
root.title("Happy Circles")

# set width and height
width = 600
height = 400
# create the Tkinter canvas for drawing
cv_tk = tk.Canvas(width=width, height=height, bg='black')
cv_tk.pack()
# create a PIL canvas in memory and use in parallel
black = (0, 0, 0)
img_pil = Image.new("RGB", (width, height), black)
cv_pil = ImageDraw.Draw(img_pil)

# camera setup
origin = (0.0, 1.0, 0.0)
lookat = (0.0, 0.0, -1.0)
up = (0.0, 1.0, 0.0)
fov = 90
aspect = width/height
camera = Camera(origin, lookat, up, fov, aspect)
n_samples = 10

# world setup
#diffuse = Sphere((0.0, 0.0, -1.0), 0.5, Lambertian((0.8, 0.3, 0.3)))
#metal = Sphere((1.0, 0.0, -1.0), 0.5, Metal((0.8, 0.6, 0.2)))
#glass = Sphere((-1.0, 0.0, -1.0), 0.5, Dielectric(1.5))
earth = Sphere((0.0, -100.5, -1.0), 100.0, Lambertian((0.8, 0.8, 0.0)))
spheres = [earth]
for i in range(-2, 3):
    for j in range(-2, 3):
        location = (0.5*i, 0.0, -1.0+0.5*j)
        material = None
        r = random.random()
        if r < 1/3:
            material = Lambertian((random.random(), random.random(), random.random()))
        elif r < 2/3:
            material = Metal((random.random(), random.random(), random.random()))
        else:
            material = Dielectric(1 + 3*random.random())
        radius = 0.1 + 0.1 * random.random()
        spheres.append(Sphere(location, radius, material))
        
world = HitableList(spheres)
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
            color_pil = tuple(int(255.99 * col[i]) for i in range(3))
            color_tk = '#' + "".join("%02x" % c for c in color_pil)
            cv_tk.create_oval((i, height-j-1, i+2, height-j-1+2),
                              fill=color_tk)
            cv_pil.point((i, height-j-1), fill=color_pil)
            root.update()
        print('drew row ' + str(j))
draw()

# start the program's event loop
# root.mainloop()
filename = "happy_circles.jpg"
img_pil.save(filename)
